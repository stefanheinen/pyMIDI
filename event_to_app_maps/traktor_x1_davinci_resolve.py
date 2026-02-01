import pyautogui
from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from devices.hid.traktor_x1_mk3 import HIDDevice as X1_HID_Device
from devices.midi.traktor_x1_mk3 import Device as X1_MIDI_Device

from event_to_app_maps.native_instruments_event_to_app_map import NIEventToAppMap

class EventToAppToAppMap(NIEventToAppMap):
    NAME = "DaVinci Resolve"
    APP_NAME_DISPLAY = 2
    HELP_BUTTON = "2:SHIFT"
    HELP_DISPLAYS = (3, 4)
    APPLICATION_NAME = "Davinci Resolve"

    def __init__(self, device: X1_HID_Device | X1_MIDI_Device):
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
        "0:LOOP:L": ("Zoom Out", "alt+scroll(-10)"),
        "0:LOOP:R": ("Zoom In", "alt+scroll(+10)"),
        "0:LOOP:L[0:LOOP]": ("Zoom Out Vertical", "shift+scroll(-10)"),
        "0:LOOP:R[0:LOOP]": ("Zoom In Vertical", "shift+scroll(+10)"),
        "1:PLAY": ("Partymode", "♪♪♪♪"),
        "1:H1": ("Select at\nPlayhead", "alt + shift + V"),
        "1:LEFT": ("Select left", "alt + cmd + Y"),
        "1:RIGHT": ("Select right", "alt + Y"),
    }

    c = Native_Instruments_HID_Device.LEDColor
    BUTTON_COLORS = {
        "0:PLAY": (c.GREEN, c.RED),
        "0:SYNC": (c.GREEN, c.RED),
        "0:H1": (c.RED, c.RED),
        "0:H2": (c.RED, c.RED),
        "0:LEFT": (c.GREEN, c.RED),
        "0:RIGHT": (c.GREEN, c.RED),
        "0:CUE": (c.RED, c.RED),
        "0:REV": (c.YELLOW, c.RED),
        "1:PLAY": (c.MAGENTA, c.RED),
        "1:H1": (c.BLUE, c.RED),
        "1:LEFT": (c.BLUE, c.RED),
        "1:RIGHT": (c.BLUE, c.RED),
    }

    def handle_event(self, event: str):
        if event == "0:LOOP:D":
            self.MOD["0:LOOP"] = True
        if event == "0:LOOP:U":
            self.MOD["0:LOOP"] = False

        super().handle_event(event)

        if self.MOD["HELP"]: return

        if not "color_cycle" in self.state: self.state["color_cycle"] = self.colorCycler(self.c)
        if event == "1:BROWSE:R":
            self.DEFAULT_BUTTON_COLORS = (self.state["color_cycle"].step(1), self.DEFAULT_BUTTON_COLORS[1])
            self.set_default_led_colors(event)
        if event == "1:BROWSE:L":
            self.DEFAULT_BUTTON_COLORS = (self.state["color_cycle"].step(-1), self.DEFAULT_BUTTON_COLORS[1])
            self.set_default_led_colors(event)

        if event == "0:BROWSE:L": pyautogui.press("left")
        if event == "0:BROWSE:R": pyautogui.press("right")
        if event == "0:BROWSE:U": pyautogui.hotkey("command", "b")

        MOD_LOOP = self.MOD["0:LOOP"]
        if event == "0:LOOP:L":
            if MOD_LOOP:
                pyautogui.keyDown('shift')
            else:
                pyautogui.keyDown('alt')
            #time.sleep(0.02)
            pyautogui.scroll(-10)
            #time.sleep(0.02)
            if not MOD_LOOP:
                pyautogui.keyUp('alt')
            else:
                pyautogui.keyUp('shift')

        if event == "0:LOOP:R":
            if MOD_LOOP:
                pyautogui.keyDown('shift')
            else:
                pyautogui.keyDown('alt')
            #time.sleep(0.02)
            pyautogui.scroll(10)
            #time.sleep(0.02)
            if not MOD_LOOP:
                pyautogui.keyUp('alt')
            else:
                pyautogui.keyUp('shift')
            
        if event == "0:PLAY:U":
            pyautogui.press("space")
            # if "playing" not in self.state: self.state["playing"] = False
            # if not self.state["playing"]:
            #     self.launch_interface_thread("blinking_play_button", self.blinky_led_thread_function, (self.device.BACKLIGHT_LEDS + ["0:PLAY"], 0.2, Native_Instruments_HID_Device.LEDColor.GREEN, Native_Instruments_HID_Device.LEDColor.GREEN_DIM))
            # else:
            #     self.stop_interface_thread("blinking_play_button")
            # self.state["playing"] = not self.state["playing"]

        if event == "0:SYNC:D":
            pyautogui.press("space")

        if event == "0:SYNC:U":
            pyautogui.press("space")

        if event == "0:H1:U": pyautogui.hotkey('shift', '[')
        if event == "0:H2:U": pyautogui.hotkey('shift', ']')

        if event == "0:LEFT:U": pyautogui.press("left")
        if event == "0:RIGHT:U": pyautogui.press("right")

        if event == "0:CUE:U": pyautogui.hotkey('command', 'b')
        if event == "0:REV:U": pyautogui.hotkey('command', 'z')


        ### Right Channel ###
        if event == "1:H1:U": pyautogui.hotkey('alt', 'shift', 'v')
        if event == "1:LEFT:U": pyautogui.hotkey('alt', 'command', 'y')
        if event == "1:RIGHT:U": pyautogui.hotkey('alt', 'y')

        if event == "1:LOOP:L": pyautogui.dragRel(-1, 0, duration=0.1, button='left')
        if event == "1:LOOP:R": pyautogui.dragRel(1, 0, duration=0.1, button='left')

        if event == "1:PLAY:U":
            if "partymode" not in self.state: self.state["partymode"] = False
            if not self.state["partymode"]:
                self.launch_interface_thread("partymode", self.cycle_led_thread_function,
                                             (list(self.device.LED_bytes.keys()),
                                              0.1,
                                              [Native_Instruments_HID_Device.LEDColor.GREEN,
                                               Native_Instruments_HID_Device.LEDColor.BLUE,
                                               Native_Instruments_HID_Device.LEDColor.YELLOW,
                                               Native_Instruments_HID_Device.LEDColor.RED,
                                               Native_Instruments_HID_Device.LEDColor.CYAN,
                                               Native_Instruments_HID_Device.LEDColor.FUCHSIA]))
            else:
                self.stop_interface_thread("partymode")
            self.state["partymode"] = not self.state["partymode"]

        self.device.flush_leds()