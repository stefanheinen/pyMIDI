import threading
from abc import abstractmethod
import queue
from queue import Queue
from threading import Thread
from logging import info, warning
import time

class Device:
    PROTOCOL: str
    DEVICE_NAME: str

    _status: str
    _lock: threading.Lock

    def __init__(self):
        self.send_thread = None
        self.send_queue = Queue()
        self.receive_thread = None
        self.receive_queue = None
        self.stop_threads = threading.Event()
        self._status = ""
        self._lock = threading.Lock()

    def get_status(self):
        with self._lock:
            return self._status

    def set_status(self, status):
        with self._lock:
            self._status = status

    ### START Device Specific Methods: These methods must be implemented by every device.
    @abstractmethod
    def _open_connected_device(self):
        pass

    @abstractmethod
    def _close_connected_device(self):
        pass

    @abstractmethod
    def _write_connected_device(self, msg):
        pass

    @abstractmethod
    def _read_connected_device(self):
        pass

    @abstractmethod
    def _request_control_status_connected_device(self):
        pass

    @abstractmethod
    def _exists_connected_device(self):
        pass

    @abstractmethod
    def decode_events(self, msg):
        pass

    @abstractmethod
    def startup(self, animation = True):
        pass
    ### END Device Specific Methods: These methods must be implemented by every device.

    def open(self, receive_queue: Queue | None):
        try:
            self._open_connected_device()
            self.set_status("connected")
        except:
            self.set_status("")
            return

        self.stop_threads.clear()
        self.send_queue = Queue()
        self.send_thread = Thread(target=self.send_thread_function, args=(self.send_queue,), daemon=True)
        self.send_thread.start()

        if receive_queue:
            self.receive_queue = receive_queue
        else:
            self.receive_queue = Queue()
        self.receive_thread = Thread(target=self.receive_thread_function, args=(self.receive_queue,), daemon=True)
        self.receive_thread.start()

    def close(self):
        self.stop_threads.set()
        time.sleep(0.3)
        self._close_connected_device()
        time.sleep(0.2)

    def send_thread_function(self, q: Queue):
        while not self.stop_threads.is_set():
            try:
                if not self._exists_connected_device():
                    time.sleep(0.2)
                    continue
                msg = q.get(timeout=0.3)
                if msg:
                    self._write_connected_device(msg)
            except queue.Empty:
                pass
            except Exception as e:
                self.set_status("disconnected")
                self.stop_threads.set()
                warning(f"{self.PROTOCOL}:{self.DEVICE_NAME}: Send Thread Exception: {str(e)}")
                break
        info(f"{self.PROTOCOL}:{self.DEVICE_NAME}: Send thread shutting down")

    def receive_thread_function(self, q):
        def process_msg(report):
            if report:
                events = self.decode_events(report)
                if events:
                    for e in events:
                        q.put((self, e))

        process_msg(self._request_control_status_connected_device())

        while not self.stop_threads.is_set():
            try:
                if not self._exists_connected_device():
                    time.sleep(0.1)
                    continue
                msg = self._read_connected_device()
                if msg:
                    process_msg(msg)
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.set_status("disconnected")
                self.stop_threads.set()
                warning(f"{self.PROTOCOL}:{self.DEVICE_NAME}: Receive Thread Exception: {str(e)}")
                break
        info(f"{self.PROTOCOL}:{self.DEVICE_NAME}: Receive thread shutting down")