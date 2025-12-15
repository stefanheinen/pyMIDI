import time
from abc import ABC, abstractmethod

import mido

import devices.device

class MIDI_Device(devices.device.Device, ABC):
    MIDI_port_name: str
    PROTOCOL = "MIDI"
    DISPLAY_SIZE: (int, int)
    DISPLAY_COUNT: int

    def __init__(self):
        super().__init__()
        self.midi_device = None

    @abstractmethod
    def decode_events(self, msg):
        pass

    @abstractmethod
    def startup(self, animation = True):
        pass

    def write_display_image(self, display: int, image):
        pass

    def clear_displays(self):
        pass

    def clear_display(self, display: int):
        pass

    def flush_leds(self):
        pass

    def text_to_display(self, display: int, text: str, font="", size=0):
        pass

    @abstractmethod
    def set_led(self, led_name: str, color):
        pass

    def _open_connected_device(self):
        self.midi_device = mido.open_ioport(self.MIDI_port_name)

    def _close_connected_device(self):
        if self.midi_device:
            self.midi_device.close()

    def _write_connected_device(self, msg):
        self.midi_device.send(msg)

    def _read_connected_device(self):
        return self.midi_device.receive(block=False)

    def _request_control_status_connected_device(self):
        return None

    def _exists_connected_device(self):
        if self.midi_device:
            return True
        else:
            return False


class MIDIEvent:
    def __init__(self, type = None, channel = None, control = None, note = None, value = None, velocity = None):
        self.type = None
        self.channel = channel
        self.control = control
        self.note = note
        self.value = value
        self.velocity = velocity

    def __eq__(self, other):
        if self.type != None and self.type != getattr(other, 'type', None):
            return False

        if self.channel != None and self.channel != getattr(other, 'channel', None):
            return False

        if self.control != None and self.control != getattr(other, 'control', None):
            return False

        if self.note != None and self.note != getattr(other, 'note', None):
            return False

        if self.value != None and self.value != getattr(other, 'value', None):
            return False

        if self.velocity != None and self.velocity != getattr(other, 'velocity', None):
            return False

        return True