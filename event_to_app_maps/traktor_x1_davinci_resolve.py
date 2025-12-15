import pyautogui
from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from devices.hid.traktor_x1_mk3 import HIDDevice as X1_Device

from event_to_app_maps.native_instruments_event_to_app_map import NIEventToAppMap

class EventToAppToAppMap(NIEventToAppMap):
    APP_NAME_DISPLAY = 2
    HELP_BUTTON = "2:SHIFT"
    HELP_DISPLAYS = (3, 4)

    def __init__(self, device: X1_Device):
        super().__init__(device)
        self.device = device

    MOD = {"0:LOOP": False}

    HELP_TEXTS = {
        "0:PLAY": ("Play/Pause", "Space"),
        "0:SYNC": ("Play/Pause", "Space"),
        "0:H1": ("Trim Left", "shift + ["),
        "0:H2": ("Trim Right", "shift + ]"),
        "0:CUE": ("Cut", "cmd + b"),
        "0:REV": ("Undo", "cmd + z"),
        "0:LEFT": ("1 Frame Left", "←"),
        "0:RIGHT": ("1 Frame Right", "→"),
        "0:BROWSE:L": ("1 Frame Left", "←"),
        "0:BROWSE:R": ("1 Frame Right", "→"),
        "0:BROWSE:D": ("Cut", "cmd + b"),
        "0:LOOP:L": ("Zoom Out", "scroll(-10)"),
        "0:LOOP:R": ("Zoom In", "scroll(+10)"),
    }

    c = Native_Instruments_HID_Device.LEDColor
    BUTTON_COLORS = {
        "0:PLAY": (c.GREEN, c.RED),
        "0:SYNC": (c.GREEN, c.RED),
        "0:H1": (c.RED, c.RED),
        "0:H2": (c.RED, c.RED),
        "0:LEFT": (c.BLUE, c.RED),
        "0:RIGHT": (c.BLUE, c.RED),
        "0:CUE": (c.RED, c.RED),
        "0:REV": (c.YELLOW, c.RED),
    }

    def init_leds(self):
        for k, v in self.BUTTON_COLORS.items():
            self.device.set_led(k, v[0])
        self.device.flush_leds()

    def handle_event(self, event: str):
        super().handle_event(event)

        if self.MOD["HELP"]: return

        if event == "0:BROWSE:L": pyautogui.press("left")
        if event == "0:BROWSE:R": pyautogui.press("right")
        if event == "0:BROWSE:U": pyautogui.hotkey("command", "b")

        if event == "0:LOOP:L":
            if self.MOD["0:LOOP"] == 0: pyautogui.keyDown('alt')
            if self.MOD["0:LOOP"] == 1: pyautogui.keyDown('shift')
            pyautogui.scroll(-10)
            if self.MOD["0:LOOP"] == 0: pyautogui.keyUp('alt')
            if self.MOD["0:LOOP"] == 1: pyautogui.keyUp('shift')
        if event == "0:LOOP:R":
            if self.MOD["0:LOOP"] == 0: pyautogui.keyDown('alt')
            if self.MOD["0:LOOP"] == 1: pyautogui.keyDown('shift')
            pyautogui.scroll(10)
            if self.MOD["0:LOOP"] == 0: pyautogui.keyUp('alt')
            if self.MOD["0:LOOP"] == 1: pyautogui.keyUp('shift')
        if event == "0:LOOP:D":
            self.MOD["0:LOOP"] = 1
        if event == "0:LOOP:U":
            self.MOD["0:LOOP"] = 0

        if event == "0:PLAY:U":
            pyautogui.press("space")

        if event == "0:SYNC:D": pyautogui.press("space")
        if event == "0:SYNC:U": pyautogui.press("space")

        if event == "0:H1:U": pyautogui.hotkey('shift', '[')
        if event == "0:H2:U": pyautogui.hotkey('shift', ']')

        if event == "0:LEFT:U": pyautogui.press("left")
        if event == "0:RIGHT:U": pyautogui.press("right")

        if event == "0:CUE:U": pyautogui.hotkey('command', 'b')
        if event == "0:REV:U": pyautogui.hotkey('command', 'z')


        ### Right Channel ###
        if event == "1:LOOP:L": pyautogui.dragRel(-1, 0, duration=0.1, button='left')
        if event == "1:LOOP:R": pyautogui.dragRel(1, 0, duration=0.1, button='left')