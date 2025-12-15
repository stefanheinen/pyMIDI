from enum import IntEnum
from PIL import Image, ImageDraw, ImageFont, ImageOps
from abc import abstractmethod
from pathlib import Path
import time
from logging import warning

from devices.hid.hid_device import HID_Device

from globals import PROJECT_ROOT

class Native_Instruments_HID_Device(HID_Device):
    previousReport: bytes | None
    LED_bytes: {}
    DISPLAY_SIZE: (int, int)
    DISPLAY_COUNT: int

    # LED color constants
    class LEDColor(IntEnum):
        BLACK = 0x00
        RED_DIM = 0x04
        RED = 0x06
        DARK_ORANGE_DIM = 0x08
        DARK_ORANGE = 0x0A
        LIGHT_ORANGE_DIM = 0x0C
        LIGHT_ORANGE = 0x0E
        WARM_ORANGE_DIM = 0x10
        WARM_YELLOW = 0x12
        YELLOW_DIM = 0x14
        YELLOW = 0x16
        LIME_DIM = 0x18
        LIME = 0x1A
        GREEN_DIM = 0x1C
        GREEN = 0x1E
        MINT_DIM = 0x20
        MINT = 0x22
        CYAN_DIM = 0x24
        CYAN = 0x26
        TURQUOISE_DIM = 0x28
        TURQUOISE = 0x2A
        BLUE_DIM = 0x2C
        BLUE = 0x2E
        PLUM_DIM = 0x30
        PLUM = 0x32
        VIOLET_DIM = 0x34
        VIOLET = 0x36
        PURPLE_DIM = 0x38
        PURPLE = 0x3A
        MAGENTA_DIM = 0x3C
        MAGENTA = 0x3E
        FUSCHIA_DARK = 0x40
        FUSCHIA = 0x42
        WHITE = 0x46

    class LEDColor_Bright(IntEnum):
        RED = 0x06
        DARK_ORANGE = 0x0A
        LIGHT_ORANGE = 0x0E
        WARM_YELLOW = 0x12
        YELLOW = 0x16
        LIME = 0x1A
        GREEN = 0x1E
        MINT = 0x22
        CYAN = 0x26
        TURQUOISE = 0x2A
        BLUE = 0x2E
        PLUM = 0x32
        VIOLET = 0x36
        PURPLE = 0x3A
        MAGENTA = 0x3E
        FUCHSIA = 0x42
        WHITE = 0x46

    @abstractmethod
    def flush_leds(self):
        pass

    def leds_off(self):
        for l in self.LED_bytes:
            self.set_led(l, self.LEDColor.BLACK)
            self.flush_leds()

    def leds_on(self, color: LEDColor):
        for l in self.LED_bytes:
            self.set_led(l, color)
            self.flush_leds()

    def shutdown(self):
        self.clear_displays()
        self.leds_off()

    def startup(self, animation = True):
        self.clear_displays()

        if animation:
            self.startup_animation()

        self.leds_on(self.LEDColor.WHITE)

    def set_led(self, led_name: str, color: LEDColor):
        if led_name in self.LED_bytes:
            self.LED_bytes[led_name] = color
        else:
            warning(f"Unknown LED: \"{led_name}\"")

    def decode_bit_byte(self, button_name:str, byte:int, bit:int, cur):
        prev = self.previousReport
        was_on = (prev[byte] & (1 << bit)) != 0
        is_on = (cur[byte] & (1 << bit)) != 0

        if not was_on and is_on:
            return button_name + ":D"
        elif was_on and not is_on:
            return button_name + ":U"
        else:
            return None

    def startup_animation(self):
        img = ImageOps.invert(self._icon_image("rocket").convert("L")).convert("1")

        for i in range(0, self.DISPLAY_COUNT):
            self.write_display_image(i, img)

        for c in self.LEDColor_Bright:
            for l in self.LED_bytes:
                self.set_led(l, c)

            self.flush_leds()
            time.sleep(0.06)

        self.clear_displays()

    ##### Display related functions
    def image_to_packed_bytes(self, img: Image.Image):
        """
        Converts a 128x64 Pillow image (mode "1") to 8-page packed bytes.
        Each page is 8 pixels high and 128 pixels wide.
        """
        width, height = img.size
        assert width == 128 and height == 64, "Image must be 128x64"
        assert img.mode == "1", "Image must be in 1-bit mode ('1')"

        px = img.load()
        pages = 8
        bytes_per_page = width
        buf = bytearray(pages * bytes_per_page)

        for page in range(pages):
            for x in range(width):
                byte = 0
                for bit in range(8):
                    y = page * 8 + bit
                    if px[x, y]:
                        byte |= (1 << bit)
                buf[page * bytes_per_page + x] = byte

        return bytes(buf)

    def write_display_image(self, display: int, img: Image.Image):
        img = ImageOps.invert(img.convert("L")).convert("1")
        bytes = self.image_to_packed_bytes(img)
        self.write_display_bytes(display, bytes)

    def write_display_bytes(self, display_number, bytes):
        part_size = len(bytes) // 4
        buf = [bytes[i * part_size: (i + 1) * part_size] for i in range(4)]

        self.send_queue.put(bytes.fromhex(f"e{display_number}0000000080000200") + buf[0])
        self.send_queue.put(bytes.fromhex(f"e{display_number}0000020080000200") + buf[1])
        self.send_queue.put(bytes.fromhex(f"e{display_number}0000040080000200") + buf[2])
        self.send_queue.put(bytes.fromhex(f"e{display_number}0000060080000200") + buf[3])

    def clear_display(self, display_number):
        self.write_display_bytes(display_number, bytes.fromhex("FF" * 1024))

    def white_display(self, display_number):
        self.write_display_bytes(display_number, bytes.fromhex("00" * 1024))

    def text_to_display(self, display: int, text: str, font="source-sans-pro/SourceSansPro-Regular.ttf", size=22):
        self.write_display_image(display, self._text_to_display_image(text, font, size))

    def _text_to_display_image(self, text, font: str, size: int):
        img = Image.new("1", (self.DISPLAY_SIZE[0], self.DISPLAY_SIZE[1]))
        draw = ImageDraw.Draw(img)

        # Draw example content
        font = ImageFont.truetype(Path(PROJECT_ROOT) / "fonts" / font, size)
        draw.text((0, 0), text, fill=1, font=font)

        return img

    def clear_displays(self):
        for i in range(0, self.DISPLAY_COUNT):
            self.clear_display(i)

    def _icon_image(self, icon: str):
        # Create the target image (128x64, 1-bit)
        background = Image.new("1", (self.DISPLAY_SIZE[0], self.DISPLAY_SIZE[1]),
                               0)  # 0 = black background

        # Load the icon
        icon = Image.open(Path(PROJECT_ROOT) / "icons" / (icon + ".png")).convert("1")

        # Scale the icon to max height 64 while keeping aspect ratio
        max_height = self.DISPLAY_SIZE[1]
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