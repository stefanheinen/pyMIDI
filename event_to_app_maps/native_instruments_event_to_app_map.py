from abc import ABC, abstractmethod
import threading
import time
from collections.abc import Iterable

from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from pathlib import Path
from PIL import Image
from globals import PROJECT_ROOT

from event_to_app_maps.event_to_app_map import EventToAppMap as EventToAppMap

class NIEventToAppMap(EventToAppMap, ABC):
    BUTTON_COLORS: {}
    HELP_BUTTON: str
    HELP_DISPLAYS: (int, int)
    APP_NAME_DISPLAY: int
    HELP_TEXTS: {}
    MOD: {}
    BUTTON_COLORS: {}
    COLORS = Native_Instruments_HID_Device.LEDColor
    DEFAULT_BUTTON_COLORS = (COLORS.WHITE, COLORS.RED)

    APPLICATION_NAME: str

    device: Native_Instruments_HID_Device

    def __init__(self, device):
        self.MOD["HELP"] = False

        self.interface_threads = {}
        self.state = {}

    def init(self):
        """
        Initializes the state the device should have after startup / being connected
        """
        self.init_leds()
        self.init_screens()

    def shutdown(self, wait=False):
        for t in self.interface_threads.values():
            t[1].set()

        if wait:
            for t in self.interface_threads.values():
                t[0].join()

    def shutdown_join(self):
        for t in self.interface_threads.values():
            t[0].join()

    def init_leds(self):
        for k, v in self.BUTTON_COLORS.items():
            self.device.set_led(k, v[0])
        self.device.flush_leds()

    def init_screens(self):
        self.device.clear_displays()
        self.device.write_text_to_display(self.APP_NAME_DISPLAY, self.APPLICATION_NAME.replace(" ", "\n"),
                                    "source-sans-pro/SourceSansPro-Bold.ttf", 25)

    def set_default_led_colors(self, event =""):
        """
        Sets the standard led colors (for example when an event comes in)
        """
        if ":" in event:
            channel, control, value = event.split(":")
        else:
            channel = ""
            control = ""
            value = ""

        for l in self.device.LED_bytes.keys():
            if f"{channel}:{control}" == l and value == "D":
                color_index = 1
            else:
                color_index = 0
            self.set_default_led_color(l, color_index)

    def set_default_led_color(self, led, color_index = 0):
        if led in self.BUTTON_COLORS:
            self.device.set_led(led, self.BUTTON_COLORS[led][color_index])
        else:
            self.device.set_led(led, self.DEFAULT_BUTTON_COLORS[color_index])


    def handle_help(self, event):
        """
        Handles the display of help texts when the HELP modifier is set.
        """
        if event == f"{self.HELP_BUTTON}:D":
            self.MOD["HELP"] = True
            self.device.write_display_image(self.HELP_DISPLAYS[1], self._icon_image("help"))
            return
        if event == f"{self.HELP_BUTTON}:U":
            #self.device.clear_display(self.HELP_DISPLAYS[0])
            #self.device.clear_display(self.HELP_DISPLAYS[1])
            self.init_screens()
            self.MOD["HELP"] = False

        if self.MOD["HELP"]:
            for k, v in self.HELP_TEXTS.items():
                # for m in self.MOD:
                #     event_mod_string = f"{event}[{m}]"
                #     if self.MOD[m] and k.startswith(f"{event}[{m}]"):
                #         self.device.text_to_display(self.HELP_DISPLAYS[0], v[0] + "\n" + v[1])
                #         return
                if event.startswith(k):
                    self.device.write_text_to_display(self.HELP_DISPLAYS[0], v[0] + "\n" + v[1])
                    return
            self.device.write_text_to_display(self.HELP_DISPLAYS[0], f"{event}\n(unassigned)")

    def handle_event(self, event: str):
        self.set_default_led_colors(event)
        self.handle_help(event)

        if not self.MOD["HELP"] and hasattr(self.device, "LED_COORDINATES"):
            channel, control, value = event.split(":")
            if value == "D" and f"{channel}:{control}" not in self.HELP_TEXTS and f"{channel}:{control}" in self.device.LED_bytes:
                self.stop_interface_thread("led_wave_thread_function")
                self.launch_interface_thread("led_wave_thread_function", self.led_wave_thread_function,
                                             (f"{channel}:{control}",
                                              self.device.LEDCOLOR_RANDOM(self.device.LEDColor_Bright),
                                              self.device.LEDCOLOR_RANDOM(self.device.LEDColor_Dim))
                                             )

    def _icon_image(self, icon:str):
        """
        Returns a pillow image that contains the centered icon from PROJECT_ROOT / icons / <icon>.png
        :param icon:
        :return:
        """
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


    ### functions for the user interface logic: blinking leds, ...
    def launch_interface_thread(self, name: str, function, args):
        stop_event = threading.Event()
        t = threading.Thread(target=function, args=(stop_event,) + args, daemon=True)
        t.start()
        self.interface_threads[name] = (t, stop_event)

    def stop_interface_thread(self, name: str):
        if name in self.interface_threads:
            self.interface_threads[name][1].set()
            return True
        return False

    def blinky_led_thread_function(self, stop_event, led: str | list[str], speed: float, on_color: Native_Instruments_HID_Device.LEDColor, off_color: Native_Instruments_HID_Device.LEDColor =  Native_Instruments_HID_Device.LEDColor.BLACK):
        self.cycle_led_thread_function(stop_event, led, speed, [on_color, off_color])

    def cycle_led_thread_function(self, stop_event, led: str | list  [str], speed: float, colors: [Native_Instruments_HID_Device.LEDColor]):
        i = 0
        if not isinstance(led, list):
            led = [led]

        while not stop_event.is_set():
            new_color = colors[i % len(colors)]
            for l in led:
                self.device.set_led(l, new_color)
            self.device.flush_leds()
            i += 1
            time.sleep(speed)

        self.set_default_led_colors()
        self.device.flush_leds()

    class colorCycler:
        def __init__(self, colors, start_index=0):
            self.items = list(colors)
            self.index = start_index % len(self.items)

        def step(self, direction=1):
            """Move in the given direction and return the new item."""
            self.index = (self.index + direction) % len(self.items)
            return self.items[self.index]

        def current(self):
            """Return the current item without moving."""
            return self.items[self.index]

    def led_wave_thread_function(self, stop_event, origin_led, color_bright, color_dim):
        step_width = 4
        step_time = 0.005

        origin_coordinates = self.device.get_led_coordinates(origin_led)

        mixer_leds = [f"0:M{x}" for x in range(1, 11)]
        mixer_leds.extend([f"1:M{x}" for x in range(1, 11)])
        leds_excluded = mixer_leds
        leds_excluded.extend(["2:SHIFT", origin_led])
        leds_for_wave = [l for l in self.device.LED_bytes if l not in leds_excluded]

        leds_with_coordinates = []
        for l in leds_for_wave:
            coordinates = self.device.get_led_coordinates(l)
            d = ( (coordinates[0] - origin_coordinates[0]) ** 2 + (coordinates[1] - origin_coordinates[1]) ** 2) ** 0.5
            leds_with_coordinates.append( (l, d) )

        color_bright_current = color_bright
        color_dim_current = color_dim
        for t in range(-30, 350, step_width):
            if stop_event.is_set(): break

            if isinstance(color_bright, Iterable):
                color_bright_current = next(color_bright)
            if isinstance(color_dim, Iterable):
                color_dim_current = next(color_dim)

            r1 = t
            r2 = t + 40
            r3 = t + 80
            r4 = t + 120

            for l in leds_with_coordinates:
                d = l[1]

                if d > r4:
                    pass
                if r4 > d > r3:
                    self.device.set_led(l[0], color_dim_current)
                if r3 > d > r2:
                    self.device.set_led(l[0], color_bright_current)
                if r2 > d > r1:
                    self.device.set_led(l[0], color_dim_current)
                if r1 > d:
                    self.set_default_led_color(l[0])

            self.device.flush_leds()
            time.sleep(step_time)

        self.init_leds()