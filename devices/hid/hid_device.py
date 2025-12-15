from abc import ABC, abstractmethod

import hid

import devices.device

class HID_Device(devices.device.Device, ABC):
    VENDOR_ID: bytes
    PRODUCT_ID: bytes
    PACKET_SIZE: int
    PROTOCOL = "HID"

    def __init__(self):
        super().__init__()
        self.hid_device = None

    @abstractmethod
    def decode_events(self, report):
        pass

    @abstractmethod
    def startup(self, animation = True):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    def _open_connected_device(self):
        self.hid_device = hid.Device(vid=self.VENDOR_ID, pid=self.PRODUCT_ID)

    def _close_connected_device(self):
        if self.hid_device:
            self.hid_device.close()

    def _write_connected_device(self, msg):
        self.hid_device.write(bytes(msg))

    def _read_connected_device(self):
        return self.hid_device.read(self.PACKET_SIZE, timeout=500)

    def _request_control_status_connected_device(self):
        return self.hid_device.get_input_report(1, self.PACKET_SIZE)

    def _exists_connected_device(self):
        if self.hid_device:
            return True
        else:
            return False