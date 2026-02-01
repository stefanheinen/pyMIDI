from abc import ABC

from devices.midi.midi_device import MIDI_Device


class Native_Instruments_MIDI_Device(MIDI_Device, ABC):
    def clear_displays(self):
        pass

    def write_text_to_display(self, display: int, text: str, font="source-sans-pro/SourceSansPro-Regular.ttf", size=22,
                              x: int = 0, y: int = 0):
        pass

    def flush_leds(self):
        pass