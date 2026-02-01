from .native_instruments_hid_device import Native_Instruments_HID_Device

class HIDDevice(Native_Instruments_HID_Device):
    # Native Instruments Z1 MK2
    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x2400
    PACKET_SIZE = 64
    DEVICE_NAME = "TRAKTOR Z1 MK2"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 3

    BACKLIGHT_LEDS = [
        "1:BACKLIGHT_1",
        "1:BACKLIGHT_2",
        "1:BACKLIGHT_3",
        "1:BACKLIGHT_4",
        "1:BACKLIGHT_5",
        "1:BACKLIGHT_6",
        "0:BACKLIGHT_6",
        "0:BACKLIGHT_5",
        "0:BACKLIGHT_4",
        "0:BACKLIGHT_3",
        "0:BACKLIGHT_2",
        "0:BACKLIGHT_1"
    ]

    def __init__(self):
        super().__init__()

        self._previousReport = [None]

        self.LED_bytes = {
            "0:M1": self.LEDColor.BLACK,
            "0:M2": self.LEDColor.BLACK,
            "0:M3": self.LEDColor.BLACK,
            "0:M4": self.LEDColor.BLACK,
            "0:M5": self.LEDColor.BLACK,
            "0:M6": self.LEDColor.BLACK,
            "0:M7": self.LEDColor.BLACK,
            "0:M8": self.LEDColor.BLACK,
            "0:M9": self.LEDColor.BLACK,
            "0:M10": self.LEDColor.BLACK,
            "1:M1": self.LEDColor.BLACK,
            "1:M2": self.LEDColor.BLACK,
            "1:M3": self.LEDColor.BLACK,
            "1:M4": self.LEDColor.BLACK,
            "1:M5": self.LEDColor.BLACK,
            "1:M6": self.LEDColor.BLACK,
            "1:M7": self.LEDColor.BLACK,
            "1:M8": self.LEDColor.BLACK,
            "1:M9": self.LEDColor.BLACK,
            "1:M10": self.LEDColor.BLACK,
            "0:MODE_MIX": self.LEDColor.BLACK,
            "0:MODE_STEMS": self.LEDColor.BLACK,
            "1:MODE_MIX": self.LEDColor.BLACK,
            "1:MODE_STEMS": self.LEDColor.BLACK,
            "0:FX_TOGGLE": self.LEDColor.BLACK,
            "1:FX_TOGGLE": self.LEDColor.BLACK,
            "2:FX1_BUTTON": self.LEDColor.BLACK,
            "2:FX2_BUTTON": self.LEDColor.BLACK,
            "2:FX3_BUTTON": self.LEDColor.BLACK,
            "2:FX4_BUTTON": self.LEDColor.BLACK,
            "2:-": self.LEDColor.BLACK,
            "2:HEADPHONE_L": self.LEDColor.BLACK,
            "2:HEADPHONE_R": self.LEDColor.BLACK,
            "0:BACKLIGHT_1": self.LEDColor.BLACK,
            "0:BACKLIGHT_2": self.LEDColor.BLACK,
            "0:BACKLIGHT_3": self.LEDColor.BLACK,
            "0:BACKLIGHT_4": self.LEDColor.BLACK,
            "0:BACKLIGHT_5": self.LEDColor.BLACK,
            "0:BACKLIGHT_6": self.LEDColor.BLACK,
            "1:BACKLIGHT_1": self.LEDColor.BLACK,
            "1:BACKLIGHT_2": self.LEDColor.BLACK,
            "1:BACKLIGHT_3": self.LEDColor.BLACK,
            "1:BACKLIGHT_4": self.LEDColor.BLACK,
            "1:BACKLIGHT_5": self.LEDColor.BLACK,
            "1:BACKLIGHT_6": self.LEDColor.BLACK
        }

    # led coordinates on the device in mm from the top left corner, ( x, y)
    LED_COORDINATES = {
        "2:FX1_BUTTON": ( 52,   172),
        "2:FX2_BUTTON": ( 73,   172),
        "2:FX3_BUTTON": ( 52,   187),
        "2:FX4_BUTTON": ( 73,   187),
        "2:-":          ( 65,   204),
        "2:HEADPHONE_L": ( 52,  223),
        "2:HEADPHONE_R": ( 73,  223),
        "0:FX_TOGGLE": ( 20,   208),
        "1:FX_TOGGLE": ( 110,  208),
        "0:MODE_MIX":    ( 13, 13),
        "0:MODE_STEMS":    ( 25, 13),
        "1:MODE_MIX":    ( 103, 13),
        "1:MODE_STEMS":    ( 114, 13),
        "1:BACKLIGHT_1": ( 94, 262),
        "1:BACKLIGHT_2": ( 94, 229),
        "1:BACKLIGHT_3": ( 94, 195),
        "1:BACKLIGHT_4": ( 94, 164),
        "1:BACKLIGHT_5": ( 94, 129),
        "1:BACKLIGHT_6": ( 94, 96),
        "0:BACKLIGHT_6": ( 32, 96),
        "0:BACKLIGHT_5": ( 32, 129),
        "0:BACKLIGHT_4": ( 32, 164),
        "0:BACKLIGHT_3": ( 32, 195),
        "0:BACKLIGHT_2": ( 32, 229),
        "0:BACKLIGHT_1": ( 32, 262),
        "0:M1": ( 52, 289),
        "0:M2": ( 52, 283),
        "0:M3": ( 52, 277),
        "0:M4": ( 52, 271),
        "0:M5": ( 52, 265),
        "0:M6": ( 52, 258),
        "0:M7": ( 52, 252),
        "0:M8": ( 52, 246),
        "0:M9": ( 52, 240),
        "0:M10": ( 52, 234),
        "1:M1": ( 77, 289),
        "1:M2": ( 77, 283),
        "1:M3": ( 77, 277),
        "1:M4": ( 77, 271),
        "1:M5": ( 77, 265),
        "1:M6": ( 77, 258),
        "1:M7": ( 77, 252),
        "1:M8": ( 77, 246),
        "1:M9": ( 77, 240),
        "1:M10": ( 77, 234),
    }

    # screen center point coordinates on the device in mm from the top left corner, ( x, y)
    SCREEN_COORDINATES = {
        "0": ( 23,   34 ),
        "1": ( 64,   34 ),
        "2": ( 117,  34 )
    }

    # screen size ( x, y)
    SCREEN_SIZES = {
        "0": ( 21, 10 ),
        "1": ( 21, 10 ),
        "2": ( 21, 10 )
    }

    def _decode_button_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        if e:=self._decode_bit_byte("0:MODE_MIX", 1, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:MODE_STEMS", 1, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:MODE", 1, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:MODE_MIX", 1, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:MODE_STEMS", 1, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:FX_TOGGLE", 1, 5, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:FX_TOGGLE", 1, 6, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:FX1_BUTTON", 1, 7, current_report): events.append(e)

        if e:=self._decode_bit_byte("2:FX2_BUTTON", 2, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:FX3_BUTTON", 2, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:FX4_BUTTON", 2, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:-", 2, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:HEADPHONE_L", 2, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:HEADPHONE_R", 2, 5, current_report): events.append(e)

        return events

    def _decode_poti_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        value = (current_report[4] << 8) | current_report[3]
        prev_value = (prev[4] << 8) | prev[3]
        if value != prev_value:
            events.append(f"0:GAIN:{value}")

        value = (current_report[6] << 8) | current_report[5]
        prev_value = (prev[6] << 8) | prev[5]
        if value != prev_value:
            events.append(f"0:HI:{value}")

        value = (current_report[8] << 8) | current_report[7]
        prev_value = (prev[8] << 8) | prev[7]
        if value != prev_value:
            events.append(f"0:MID:{value}")

        value = (current_report[10] << 8) | current_report[9]
        prev_value = (prev[10] << 8) | prev[9]
        if value != prev_value:
            events.append(f"0:LOW:{value}")

        value = (current_report[12] << 8) | current_report[11]
        prev_value = (prev[12] << 8) | prev[11]
        if value != prev_value:
            events.append(f"0:FX:{value}")

        value = (current_report[14] << 8) | current_report[13]
        prev_value = (prev[14] << 8) | prev[13]
        if value != prev_value:
            events.append(f"1:GAIN:{value}")

        value = (current_report[16] << 8) | current_report[15]
        prev_value = (prev[16] << 8) | prev[15]
        if value != prev_value:
            events.append(f"1:HI:{value}")

        value = (current_report[18] << 8) | current_report[17]
        prev_value = (prev[18] << 8) | prev[17]
        if value != prev_value:
            events.append(f"1:MID:{value}")

        value = (current_report[20] << 8) | current_report[19]
        prev_value = (prev[20] << 8) | prev[19]
        if value != prev_value:
            events.append(f"1:LOW:{value}")

        value = (current_report[22] << 8) | current_report[21]
        prev_value = (prev[22] << 8) | prev[21]
        if value != prev_value:
            events.append(f"1:FX:{value}")

        value = (current_report[24] << 8) | current_report[23]
        prev_value = (prev[24] << 8) | prev[23]
        if value != prev_value:
            events.append(f"2:HP_MIX:{value}")

        value = (current_report[26] << 8) | current_report[25]
        prev_value = (prev[26] << 8) | prev[25]
        if value != prev_value:
            events.append(f"2:MAIN:{value}")

        value = (current_report[28] << 8) | current_report[27]
        prev_value = (prev[28] << 8) | prev[27]
        if value != prev_value:
            events.append(f"2:HP_VOL:{value}")

        value = (current_report[30] << 8) | current_report[29]
        prev_value = (prev[30] << 8) | prev[29]
        if value != prev_value:
            events.append(f"0:FADER:{value}")

        value = (current_report[32] << 8) | current_report[31]
        prev_value = (prev[32] << 8) | prev[31]
        if value != prev_value:
            events.append(f"1:FADER:{value}")

        value = (current_report[34] << 8) | current_report[33]
        prev_value = (prev[34] << 8) | prev[33]
        if value != prev_value:
            events.append(f"2:FADER:{value}")

        return events

    def decode_events(self, current_report):
        events = []

        if self._get_previous_report(current_report) is None:
            self._set_previous_report(current_report)
            return []

        if current_report == self._get_previous_report(current_report):
            return []

        events.extend(self._decode_button_events(current_report))
        events.extend(self._decode_poti_events(current_report))

        self._set_previous_report(current_report)

        # if the event has not been mapped, print the raw hid report to help with mapping
        if not events:
            print(" ".join(f"{i:02d}:{x:03d}" for i, x in enumerate(list(current_report))))

        return events

    def flush_leds(self):
        if self.LED_bytes == self._last_led_bytes:
            return

        self._last_led_bytes = self.LED_bytes.copy()

        report_bytes = list(self.LED_bytes.values())
        report_bytes.insert(0, 0x80)
        report_bytes.insert(23, 0x00)

        report_bytes = bytes(report_bytes)
        if report_bytes:
            self.send_queue.put(report_bytes)

    def mixer_leds_from_value(self, channel, fader_value: int):
        led_level = int(int(fader_value) * 11 / 4095)

        channel = int(channel)

        for l in range(0, 10):
            current_key, current_value = list(self.LED_bytes.items())[channel * 10 + l]

            if led_level > l:
                if current_value == True:
                    pass
                else:
                    self.LED_bytes[current_key] = self.LEDColor.WHITE
            else:
                if current_value == False:
                    pass
                else:
                    self.LED_bytes[current_key] = self.LEDColor.BLACK

        self.flush_leds()

    def mixer_leds_from_fader(self):
        prev = self._get_previous_report(bytes([1]))
        if prev:
            value0 = (prev[30] << 8) | prev[29]
            value1 = (prev[32] << 8) | prev[31]
            self.mixer_leds_from_value(0, value0)
            self.mixer_leds_from_value(1, value1)

    def startup_animation(self):
        super().startup_animation()
        self.mixer_leds_from_fader()