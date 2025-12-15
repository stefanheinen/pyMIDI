from .native_instruments_hid_device import Native_Instruments_HID_Device

class HIDDevice(Native_Instruments_HID_Device):
    # Native Instruments Z1 MK2
    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x2400
    PACKET_SIZE = 64
    DEVICE_NAME = "TRAKTOR Z1 MK2"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 3

    def __init__(self):
        super().__init__()

        self.previousReport = None

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

    def decode_button_events(self, cur):
        events = []

        if e:=self.decode_bit_byte("0:MODE_MIX", 0, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("0:MODE_STEMS", 0, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("2:MODE", 0, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("1:MODE_MIX", 0, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("1:MODE_STEMS", 0, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("0:FX_TOGGLE", 0, 5, cur): events.append(e)
        if e:=self.decode_bit_byte("1:FX_TOGGLE", 0, 6, cur): events.append(e)
        if e:=self.decode_bit_byte("2:FX1_BUTTON", 0, 7, cur): events.append(e)

        if e:=self.decode_bit_byte("2:FX2_BUTTON", 1, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("2:FX3_BUTTON", 1, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("2:FX4_BUTTON", 1, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("2:-", 1, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("2:HEADPHONE_L", 1, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("2:HEADPHONE_R", 1, 5, cur): events.append(e)

        return events

    def decode_poti_events(self, current):
        events = []
        prev = self.previousReport

        value = (current[3] << 8) | current[2]
        prev_value = (prev[3] << 8) | prev[2]
        if value != prev_value:
            events.append(f"0:GAIN:{value}")

        value = (current[5] << 8) | current[4]
        prev_value = (prev[5] << 8) | prev[4]
        if value != prev_value:
            events.append(f"0:HI:{value}")

        value = (current[7] << 8) | current[6]
        prev_value = (prev[7] << 8) | prev[6]
        if value != prev_value:
            events.append(f"0:MID:{value}")

        value = (current[9] << 8) | current[8]
        prev_value = (prev[9] << 8) | prev[8]
        if value != prev_value:
            events.append(f"0:LOW:{value}")

        value = (current[11] << 8) | current[10]
        prev_value = (prev[11] << 8) | prev[10]
        if value != prev_value:
            events.append(f"0:FX:{value}")

        value = (current[13] << 8) | current[12]
        prev_value = (prev[13] << 8) | prev[12]
        if value != prev_value:
            events.append(f"1:GAIN:{value}")

        value = (current[15] << 8) | current[14]
        prev_value = (prev[15] << 8) | prev[14]
        if value != prev_value:
            events.append(f"1:HI:{value}")

        value = (current[17] << 8) | current[16]
        prev_value = (prev[17] << 8) | prev[16]
        if value != prev_value:
            events.append(f"1:MID:{value}")

        value = (current[19] << 8) | current[18]
        prev_value = (prev[19] << 8) | prev[18]
        if value != prev_value:
            events.append(f"1:LOW:{value}")

        value = (current[21] << 8) | current[20]
        prev_value = (prev[21] << 8) | prev[20]
        if value != prev_value:
            events.append(f"1:FX:{value}")

        value = (current[23] << 8) | current[22]
        prev_value = (prev[23] << 8) | prev[22]
        if value != prev_value:
            events.append(f"2:HP_MIX:{value}")

        value = (current[25] << 8) | current[24]
        prev_value = (prev[25] << 8) | prev[24]
        if value != prev_value:
            events.append(f"2:MAIN:{value}")

        value = (current[27] << 8) | current[26]
        prev_value = (prev[27] << 8) | prev[26]
        if value != prev_value:
            events.append(f"2:HP_VOL:{value}")

        value = (current[29] << 8) | current[28]
        prev_value = (prev[29] << 8) | prev[28]
        if value != prev_value:
            events.append(f"0:FADER:{value}")

        value = (current[31] << 8) | current[30]
        prev_value = (prev[31] << 8) | prev[30]
        if value != prev_value:
            events.append(f"1:FADER:{value}")

        value = (current[33] << 8) | current[32]
        prev_value = (prev[33] << 8) | prev[32]
        if value != prev_value:
            events.append(f"2:FADER:{value}")

        return events

    def decode_events(self, current):
        current = current[1:]
        events = []

        if current == self.previousReport:
            return []

        if not self.previousReport:
            self.previousReport = current
            return []

        events.extend(self.decode_button_events(current))
        events.extend(self.decode_poti_events(current))

        self.previousReport = current

        # if the event has not been mapped, print the raw hid report to help with mapping
        if not events:
            print(list(current))

        return events

    def flush_leds(self):
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
        if self.previousReport:
            value0 = (self.previousReport[29] << 8) | self.previousReport[28]
            value1 = (self.previousReport[31] << 8) | self.previousReport[30]
            self.mixer_leds_from_value(0, value0)
            self.mixer_leds_from_value(1, value1)

    def startup_animation(self):
        super().startup_animation()
        self.mixer_leds_from_fader()