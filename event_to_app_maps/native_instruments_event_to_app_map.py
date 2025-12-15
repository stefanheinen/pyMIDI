from abc import abstractmethod

from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from pathlib import Path
from PIL import Image
from globals import PROJECT_ROOT

import event_to_app_maps.event_to_app_map

class NIEventToAppMap(event_to_app_maps.event_to_app_map.EventToAppMap):
    BUTTON_COLORS: {}
    HELP_BUTTON: str
    HELP_DISPLAYS: (int, int)
    APP_NAME_DISPLAY: int
    HELP_TEXTS: {}
    MOD: {}

    APPLICATION_NAME = "Davinci Resolve"

    device: Native_Instruments_HID_Device

    def __init__(self, device):
        self.MOD["HELP"] = False

    def event_button_colors(self, event):
        ### Button colors ###
        for k, v in self.BUTTON_COLORS.items():
            channel, control, value = event.split(":")
            if event.startswith(k):
                if value == "U":
                    self.device.set_led(f"{channel}:{control}", v[0])
                if value == "D":
                    self.device.set_led(f"{channel}:{control}", v[1])
                self.device.flush_leds()

    def handle_help(self, event):
        ### Handle Help Texts ###
        if event == f"{self.HELP_BUTTON}:D":
            self.MOD["HELP"] = True
            self.device.write_display_image(self.HELP_DISPLAYS[1], self._icon_image("help"))
            return
        if event == f"{self.HELP_BUTTON}:U":
            self.device.clear_display(self.HELP_DISPLAYS[0])
            self.device.clear_display(self.HELP_DISPLAYS[1])
            self.MOD["HELP"] = False

        if self.MOD["HELP"]:
            for k, v in self.HELP_TEXTS.items():
                if event.startswith(k):
                    self.device.text_to_display(self.HELP_DISPLAYS[0], v[0] + "\n" + v[1])
                    return
            self.device.text_to_display(self.HELP_DISPLAYS[0], f"{event}\n(unassigned)")

    def handle_event(self, event: str):
        self.event_button_colors(event)
        self.handle_help(event)

    def _icon_image(self, icon:str):
        # Create the target image (128x64, 1-bit)
        background = Image.new("1", (self.device.DISPLAY_SIZE[0], self.device.DISPLAY_SIZE[1]), 0)  # 0 = black background

        # Load the icon
        icon = Image.open(Path(PROJECT_ROOT) / "icons" / (icon + ".png")).convert("1")

        # Scale the icon to max height 64 while keeping aspect ratio
        max_height = self.device.DISPLAY_SIZE[1]
        w, h = icon.size
        if h > max_height:
            # Calculate new width to maintain aspect ratio
            new_w = int(w * (max_height / h))
            new_h = max_height
            icon = icon.resize((new_w, new_h), Image.LANCZOS)

        # Calculate position to center the icon
        x = (background.width - icon.width) // 2
        y = (background.height - icon.height) // 2

        # Paste the icon onto the target image
        background.paste(icon, (x, y))

        return background

    @abstractmethod
    def init_leds(self):
        pass

    def init_screens(self):
        self.device.clear_displays()
        self.device.text_to_display(self.APP_NAME_DISPLAY, self.APPLICATION_NAME.replace(" ", "\n"), "source-sans-pro/SourceSansPro-Bold.ttf", 25)


    def init(self):
        self.init_leds()
        self.init_screens()