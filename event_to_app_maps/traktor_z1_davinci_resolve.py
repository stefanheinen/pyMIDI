import pyautogui
from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from devices.hid.traktor_z1_mk2 import HIDDevice as Z1_Device

from event_to_app_maps.native_instruments_event_to_app_map import NIEventToAppMap

class EventToAppToAppMap(NIEventToAppMap):
    APP_NAME_DISPLAY = 2
    HELP_BUTTON = "2:MODE"
    HELP_DISPLAYS = (0, 1)

    MOD = {}

    def __init__(self, device: Z1_Device):
        super().__init__(device)
        self.device = device

    def handle_event(self, event: str):
        super().handle_event(event)

        channel, control, value = event.split(":")
        if control == "FADER":
            self.device.mixer_leds_from_fader()

        if self.MOD["HELP"]: return

    HELP_TEXTS = {
        # "0:MODE_MIX": ("Left Mix", "(unassigned)"),
        # "0:MODE_STEMS": ("Left Stems", "(unassigned)"),
        # "1:MODE_MIX": ("Right Mix", "(unassigned)"),
        # "1:MODE_STEMS": ("Right Stems", "(unassigned)"),
        # "0:FX_TOGGLE": ("Left FX Btn", "(unassigned)"),
        # "1:FX_TOGGLE": ("Right FX Btn", "(unassigned)"),
        # "2:FX1": ("FX 1", "(unassigned)"),
        # "2:FX2": ("FX 2", "(unassigned)"),
        # "2:FX3": ("FX 3", "(unassigned)"),
        # "2:FX4": ("FX 4", "(unassigned)"),
        # "2:-": ("Filter", "(unassigned)"),
        # "2:HEADPHONE_L": ("Left Headp", "(unassigned)"),
        # "2:HEADPHONE_R": ("Right Headp", "(unassigned)"),
    }

    c = Native_Instruments_HID_Device.LEDColor
    BUTTON_COLORS = {
        "0:MODE_MIX": (c.GREEN, c.RED),
        "0:MODE_STEMS": (c.GREEN, c.RED),
        "1:MODE_MIX": (c.GREEN, c.RED),
        "1:MODE_STEMS": (c.GREEN, c.RED),
        "0:FX_TOGGLE": (c.BLUE, c.RED),
        "1:FX_TOGGLE": (c.BLUE, c.RED),
        "2:FX1_BUTTON": (c.YELLOW, c.RED),
        "2:FX2_BUTTON": (c.YELLOW, c.RED),
        "2:FX3_BUTTON": (c.YELLOW, c.RED),
        "2:FX4_BUTTON": (c.YELLOW, c.RED),
        "2:-": (c.YELLOW, c.RED),
        "2:HEADPHONE_L": (c.WHITE, c.RED),
        "2:HEADPHONE_R": (c.WHITE, c.RED),
    }

    def init_leds(self):
        for k, v in self.BUTTON_COLORS.items():
            self.device.set_led(k, v[0])
        self.device.mixer_leds_from_fader()
        self.device.flush_leds()