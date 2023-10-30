from zeroconf.asyncio import AsyncZeroconf
import requests
import threading
import time
import itertools
import os
import asyncio
import simplejpeg
import cv2

TYPE_HTTP = '_ctl-http._tcp.local.'
TYPE_MJPEG = '_mjpeg._udp.local.'
TYPE_CTL = '_control-socket._udp.local.'

class RobotProtocol:

    def __init__(self, robot, loop):
        self.robot = robot
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.robot.ctl_ready = True
        for i in range(len(self.robot.tx_queue)):
            # In case some messages were sent before awaiting socket open
            self.robot.tx_queue[i] = (self.robot.tx_queue[i][0], time.time())
        transport.sendto("WAKE".encode("ascii"))
        self.robot.ctl_tx_thread = threading.Thread(target=asyncio.run, args=(self.robot._ctl_tx_worker(self),))
        self.robot.ctl_tx_thread.start()

    def datagram_received(self, data, addr):
        try:
            self.robot._handle_message(data.decode("ascii"))
        except:
            pass

    def error_received(self, exc):
        print('!!! Error received:', exc)

    def connection_lost(self, exc):
        print("!!! Socket closed")

class CameraProtocol:

    def __init__(self, robot, loop):
        self.robot = robot
        self.loop = loop

    def connection_made(self, transport):
        self.robot.camera_transport = transport
        transport.sendto("startstream".encode("ascii"))

    def datagram_received(self, data, addr):
        n = len(data)
        # JPEG start is FF D8 FF
        if n >= 2 and data[0] == 0xff and data[1] == 0xd8 and data[2] == 0xff:
            self.robot.in_buf = data
        else:
            self.robot.in_buf += data

        # JPEG file end, try parsing frame, swap if OK
        if n >= 2 and data[n - 2] == 0xff and data[n - 1] == 0xd9:
            try:
                recv = simplejpeg.decode_jpeg(self.robot.in_buf, colorspace = self.robot.colorspace)
                if not len(recv):
                    if self.robot.verbose:
                        print("Frame is empty")
                    return
                self.robot.fb = recv
                ts = time.time()
                self.robot.frametime = ts - self.robot.frame_ts
                self.robot.frame_ts = ts
                if self.robot.on_frame:
                    self.robot.on_frame(self.robot, recv, ts)
            except Exception as e:
                if self.robot.verbose:
                    print("Error decoding: " + str(e))

    def error_received(self, exc):
        print('!!! Camera error received:', exc)

    def connection_lost(self, exc):
        print("!!! Camera socket closed")

class Robot():

    def __init__(self, h, ma, mp, ca, cp):
        self.http_addr = h
        self.mjpeg_addr = ma
        self.mjpeg_port = mp
        self.ctl_addr = ca
        self.ctl_port = cp
        self.in_buf = []
        self.fb = []
        self.frametime = -1
        self.frame_ts = -1
        self.ctl_thread = None
        self.ctl_ready = False
        self.busy = False
        self.driving = False
        self._lock = threading.Lock()
        self.prev_tx = -1
        self.busy_timeout = 0
        self.busy_set = 0
        self.camera_thread = None
        self.camera_transport = None
        self.camera_loop = None
        self.cam_ping = 0
        # User-defined callback, must be fast
        # Guaranteed to run on a valid frame (numpy matrix)
        # Args: robot, frame, frame acquisition timestamp
        self.on_frame = None
        self.wake_timer = 0
        self.closing = False
        self.count = itertools.count()
        self.queue = {}
        self.tx_queue = []
        self.vbatt = None
        self.path = None
        self.verbose = False
        # Video window
        self._video_open = False
        self.video_thread = None
        self.colorspace = "BGR"

    def from_zeroconf(http_info, mjpeg_info, ctl_info):
        h = None
        m = None
        ca = None
        cp = None

        if len(http_info.parsed_scoped_addresses()) > 0:
            h = http_info.parsed_scoped_addresses(
            )[0] + ':' + str(http_info.port)
        else:
            print("Couldn't resolve HTTP address")
            return None

        if len(mjpeg_info.parsed_scoped_addresses()) > 0:
            ma = mjpeg_info.parsed_scoped_addresses()[0]
            mp = mjpeg_info.port
        else:
            print("Couldn't resolve MJPEG address")
            return None

        if len(ctl_info.parsed_scoped_addresses()) > 0:
            ca = ctl_info.parsed_scoped_addresses()[0]
            cp = ctl_info.port
        else:
            print("Couldn't resolve CTL address")
            return None

        return Robot(h, ma, mp, ca, cp)

    def discover(hostname):
        """
        Takes robot hostname used to find in on network using Zeroconf
        :return: A new Robot instance
        """
        zc = AsyncZeroconf()
        loop = asyncio.get_event_loop()

        http_info = None
        mjpeg_info = None
        ctl_info = None

        try:
            http_info = loop.run_until_complete(zc.async_get_service_info(
                TYPE_HTTP, hostname + '.' + TYPE_HTTP))
            mjpeg_info = loop.run_until_complete(zc.async_get_service_info(
                TYPE_MJPEG, hostname + '.' + TYPE_MJPEG))
            ctl_info = loop.run_until_complete(zc.async_get_service_info(
                TYPE_CTL, hostname + '.' + TYPE_CTL))
        finally:
            # For some reason, this can be very slow
            # loop.run_until_complete(zc.async_close())
            loop.close()

        if not (http_info and mjpeg_info and ctl_info):
            print(f"Device {hostname} unavailable")
            return None

        return Robot.from_zeroconf(http_info, mjpeg_info, ctl_info)

    def set_control(self, ctl, val):
        """
        Set video controls
        :param ctl: Control name to set
        :param val: Value
        :return: True if successful
        """
        try:
            requests.get('http://' + self.http_addr +
                         "/control?" + ctl + "=" + str(val))
            return True
        except:
            return False

    def capture(self, timeout = 3):
        """
        Capture a frame from camera
        :param timeout: timeout to wait for the first frame
        :return: a numpy matrix usable with OpenCV, in BGR colorspace
        """
        if not self.camera_thread or not self.camera_transport:
            return []

        # Remind our socket address in case camera
        # resets or network conditions change
        # Also will help when we add idle suspend
        if time.time() > self.cam_ping + 5:
            self.camera_transport.sendto("sendframes".encode("ascii"))
            self.cam_ping = time.time()

        if not len(self.fb):
            start = time.time()
            while not len(self.fb) and time.time() < start + timeout:
                time.sleep(0.05)

            if not len(self.fb):
                raise Exception('Timed out waiting for images')
                return []

        return self.fb

    def _handle_message(self, message):
        if self.verbose:
            print('[' + str(time.time()) + '] ' + message)

        if message[0] != '/' and not "wsping" in message:
            return

        if message.startswith("/E"):
            if time.time() > self.busy_set + 1:
                self.busy = False
            topic = message.split(";")[1]
            val = int(message.split(";")[2].split("/")[0])

            if topic == "vbatt":
                self.vbatt = val
            elif topic == "path":
                self.path = val
        elif message.startswith("/R"):
            if time.time() > self.busy_set + 1:
                self.busy = False
            seq = int(message.split("R")[1].split(";")[0])
            self.queue[seq] = message.split(";", 1)[1].split("/")[0]
        # wsping is returned as-is by ESP
        elif message.startswith("C"):
            seq = int(message.split("C")[1].split(";")[0])
            self.queue[seq] = message.split(";", 1)[1].split("/")[0]
        else:
            if time.time() > self.busy_set + 1:
                self.busy = False
            print('[' + str(time.time()) + '] unknown message ' + message)

    async def _ctl_tx_worker(self, protocol):
        while True:
            if self.closing:
                protocol.loop.stop()
                self.ctl_ready = False
                return

            if not self.ctl_ready:
                continue

            if self.busy and time.time() > self.busy_timeout:
                self.busy = False

            if not self.locked():
                # Assert control presence to avoid robot halting
                if (time.time() > self.wake_timer + 1
                    and not len(self.tx_queue)
                    and not self.busy):
                    self.wake_timer = time.time()
                    if self.verbose:
                        print("Sending WAKE")
                    # Ensure at least 10 ms between transmissions
                    while time.time() < self.prev_tx + 0.01:
                        time.sleep(0.001)
                    self.lock()
                    protocol.transport.sendto("WAKE".encode("ascii"))
                    self.unlock()
                    self.prev_tx = time.time()
                    continue

            if len(self.tx_queue) > 0:
                tx = self.tx_queue.pop(0)
                if time.time() > tx[1] + 5:
                    continue
                # Ensure at least 10 ms between transmissions
                while time.time() < self.prev_tx + 0.01:
                    time.sleep(0.001)
                protocol.transport.sendto(tx[0].encode("ascii"))
                self.prev_tx = time.time()

            # Make Python not hang on Windows
            time.sleep(0.002)

    def lock(self):
        """
        Acquire a lock allowing for an operation you aren't waiting for. Requires to be unlocked later
        :return: True if success
        """
        self._lock.acquire()

    def unlock(self):
        """
        Unlock after a long-running task
        """
        if self._lock.locked():
            self._lock.release()

    def locked(self):
        """
        Check if robot is busy executing
        :return: True if busy
        """
        return self._lock.locked()

    def open_control(self):
        """
        Start a process to send commands to the robot
        :return: True if success
        """
        self.closing = False
        if not self.ctl_thread:
            loop = asyncio.new_event_loop()
            connect = loop.create_datagram_endpoint(
                lambda: RobotProtocol(self, loop),
                remote_addr=(self.ctl_addr, self.ctl_port))
            loop.run_until_complete(connect)
            self.ctl_thread = threading.Thread(target=loop.run_forever)
            self.ctl_thread.start()

            start = time.time()
            while time.time() < start + 10:
                time.sleep(0.1)
                if self.ctl_ready:
                    self._ctl_init()
                    return True

            print("Timed out waiting for control socket")
            return False
        else:
            return True

    def _ctl_init(self):
        """
        Sets default control values
        """
        self.front_lights(True)
        self.back_lights(False)
        if not self.set_speed(30):
            print("WARN: Failed to set initial speed")
        if not self.ok_retry("thr;24"):
            print("WARN: Failed to set tunables")
        if not self.ok_retry("br;1"):
            print("WARN: Failed to set brake mode")
        if not self.ok_retry("brt;1000"):
            print("WARN: Failed to set brake time")

    def open_camera(self):
        """
        Start the robot camera
        :return:
        """
        if self.camera_thread:
            return

        loop = asyncio.new_event_loop()
        connect = loop.create_datagram_endpoint(
            lambda: CameraProtocol(self, loop),
            remote_addr=(self.mjpeg_addr, self.mjpeg_port))
        loop.run_until_complete(connect)
        self.camera_loop = loop
        self.camera_thread = threading.Thread(target=loop.run_forever)
        self.camera_thread.start()

    def close(self):
        """
        End communicating with the robot
        :return:
        """
        self.front_lights(False)
        time.sleep(1)
        self.closing = True
        if self.camera_loop:
            self.camera_loop.stop()

    def post(self, cmd):
        """
        Send command to robot, returns command ID you can use to check status. None if error occured
        :param cmd: command
        :return: sequential ID or None
        """
        if not self.ctl_ready:
            print("Trying to submit into a closed connection")
            return None

        seq = next(self.count)
        msg = "C{};{}".format(seq, cmd)
        if self.verbose:
            print("Submitting: " + msg)

        self.tx_queue.append((msg, time.time()))
        return seq

    def result(self, seq):
        """
        Check status of command send using post. Removes result once it has been acquired
        :param seq: Sequential ID of the command to check
        :return: String or None
        """
        if not seq in self.queue:
            return None
        else:
            return self.queue.pop(seq)

    def await_status(self, seq, timeout=2, do_log=True):
        """
        Waits for return of command send by post until timeout
        :param seq: Sequential ID of the command to check
        :param timeout: timeout to wait for
        :return: String or None
        """
        start = time.time()

        while (time.time() < start + timeout
            and not self.closing):
            result = self.result(seq)
            if result:
                return result
            time.sleep(0.01)

        if do_log:
            print(
                "Command #{} timed out after {} s".format(
                    seq, timeout))
        return None

    def submit(self, cmd, timeout=2, do_log=True):
        """
         Submit command and wait for completion until timeout
         If timeout < 0: just posts cmd, without waiting
        :param cmd: command to send
        :param timeout: timeout to wait for
        :return: Status or None
        """
        seq = self.post(cmd)
        if timeout > 0:
            self.busy = True
            self.busy_set = time.time()
            self.busy_timeout = time.time() + timeout
        if timeout <= 0:
            return seq

        return self.await_status(seq, timeout, do_log)

    def ok_cmd(self, cmd, timeout=2, do_log=True):
        """
        Submit and wait for reply containing OK, warn otherwise. Returns True, False or command ID in case of timeout < 0 (not waiting)
        :param cmd: command to send
        :param timeout: timeout to wait for
        :return: True, False or seq ID
        """
        ret = self.submit(cmd, timeout, do_log)
        if timeout <= 0:
            # seq id
            return ret

        if not ret or not ret.startswith("ok"):
            if do_log:
                print(cmd + " error: " + str(ret))
            return False

        return True

    def ok_retry(self, cmd, timeout=2):
        """
        ok_cmd with retries
        :param cmd: command to send
        :param timeout: max timeout to wait for
        :return: True, False or seq ID
        """
        res = False
        tmo = timeout * 0.1

        while not res and tmo <= timeout:
            tmo = tmo * 2
            res = self.ok_cmd(cmd, tmo, tmo > timeout / 2)

        return res

    # 0-2
    def _loglevel(self, val, timeout=2):
        self.verbose = True
        return self.ok_retry("loglevel;" + str(val), timeout)

    # 0/1
    def _esp_log(self, val, timeout=2):
        self.verbose = True
        return self.ok_retry("esp_log;" + str(val), timeout)

    def _stall_timeout(self, val, timeout=2):
        return self.ok_retry("stall_timeout;" + str(val), timeout)

    def set_speed(self, val, timeout=2):
        """
        Set robot drive speed
        :param val: -100 -- 100
        :param timeout: timeout to wait for
        :return: bool
        """
        if val < -100 or val > 100:
            print("Wrong speed value: " + str(val))
            return False

        return self.ok_retry("speed;" + str(val), timeout)

    def steer(self, val, timeout=2):
        """
        Steer (use while driving continuously)
        :param val: positive, negative or 0
        :param timeout: timeout to wait for
        :return: bool
        """
        return self.ok_retry("steer;" + str(val), timeout)

    def drive(self, timeout=2):
        """
        Drive until stopped
        :param timeout: timeout to wait for
        :return: bool
        """
        if self.driving:
            return True

        self.driving = self.ok_retry("run;", timeout)
        return self.driving

    def turn(self, val, timeout=2):
        """
        Turn until stopped
        :param val: positive, negative or 0
        :param timeout: timeout to wait for
        :return: bool
        """
        return self.drive(timeout) and self.steer(val, timeout)

    def stop(self, timeout=2):
        """
        Stops the robot, use after drive
        :param timeout: timeout to wait for
        :return: bool
        """
        self.driving = False

        a = self.steer(0, timeout)
        b = self.ok_retry("stop;", timeout)
        return a and b

    def drive_time(self, duration, timeout=2):
        """
        Drive until stopped
        :param duration: timeout to drive for
        :param timeout: timeout to wait for
        :return: bool
        """
        if duration <= 0:
            print("drive_time: duration must be a positive value in seconds")
            return False

        if not self.drive(timeout):
            self.stop(timeout / 2)
            return False
        time.sleep(duration)
        return self.stop(timeout)

    def turn_time(self, val, duration, timeout=2):
        """
        Turn until stopped
        :param val: positive, negative or 0
        :param duration: timeout to turn for
        :param timeout: timeout to wait for
        :return: bool
        """
        if duration <= 0:
            print("turn_time: duration must be a positive value in seconds")
            return False

        if not self.turn(val, timeout):
            self.stop(timeout / 2)
            return False
        time.sleep(duration)
        return self.stop(timeout)

    def drive_mm(self, val, timeout=0):
        """
        Drives for x millimeters
        :param val: mm to drive
        :param timeout: timeout to wait for
        :return: bool
        """
        if val < 0:
            print("Wrong drive path: " + str(val))
            return False

        # Calculate by default, but let custom params incl < 0
        if timeout == 0:
            timeout = 2 + val * 0.15

        # timeout as in bridge +2s
        return self.ok_cmd("drive;" + str(val), timeout)

    def turn_deg(self, val, timeout=10):
        """
        Turn for specified number of degrees
        :param val: degrees
        :param timeout: timeout to wait for
        :return: bool
        """
        return self.ok_cmd("turn;" + str(val), timeout)

    def ping(self):
        """
        Ping the STM (full control delay)
        :return: latency in ms
        """
        start = time.time()
        ret = self.submit("ping;", 3)
        end = time.time()
        if not ret or not ret.startswith("ok"):
            print("Ping error: " + str(ret))
            return -1

        return (end - start) * 1000

    def set_gpio(self, gpio, val):
        """
        Set GPIOs used for lights
        :param gpio: 1-3, pin number
        :param val: 0 or 1, value to be written
        """
        cmd = "s{};".format(gpio)
        if val:
            cmd = cmd + "1"
        else:
            cmd = cmd + "0"

        # Erratum: STM firmware doesn't reply to these commands.
        # Send redundant commands, don't wait for replies
        self.post(cmd)
        time.sleep(0.01)
        self.post(cmd)
        time.sleep(0.01)
        self.post(cmd)
        return True

    def front_lights(self, val):
        """
        Set front lights state
        :param val: whether to turn lights on or off
        """
        return self.set_gpio(3, val)

    def back_lights(self, val):
        """
        Set back lights state
        :param val: whether to turn lights on or off
        """
        return self.set_gpio(2, val)

    def ctl_ping(self):
        """
        Ping the ESP (network communication delay)
        :return: latency in ms
        """
        start = time.time()
        ret = self.submit("wsping;", 3)
        end = time.time()
        if not ret or not "wsping" in ret:
            print("Ping error: " + str(ret))
            return -1

        return (end - start) * 1000

    def _video_worker(self):
        while True:
            if self.closing:
                return

            try:
                frame = self.capture()
                if not len(frame):
                    continue

                cv2.imshow('Video', frame)
                self._video_open = True
            except Exception as e:
                print('Capture error: ' + str(e))
                return

            if cv2.waitKey(1) == 27:
                return

    def show_video(self, timeout = 5):
        """
        Open a video streaming window
        :return: True if opened successfully
        """
        if self.video_thread:
            return True

        self.open_camera()
        time.sleep(0.5)
        self.video_thread = threading.Thread(target=self._video_worker)
        self.video_thread.start()

        started = time.time()
        while time.time() < started + 5:
            if self._video_open:
                return True

        return False
