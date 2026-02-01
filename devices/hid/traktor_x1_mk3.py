from .native_instruments_hid_device import Native_Instruments_HID_Device

class HIDDevice(Native_Instruments_HID_Device):
    # Native Instruments X1 MK3
    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x2200
    PACKET_SIZE = 64
    DEVICE_NAME = "TRAKTOR X1 MK3"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 5

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
            "2:SHIFT": self.LEDColor.BLACK,
            "0:LOOP": self.LEDColor.BLACK,
            "1:LOOP": self.LEDColor.BLACK,
            "0:PLAY": self.LEDColor.BLACK,
            "0:SYNC": self.LEDColor.BLACK,
            "1:PLAY": self.LEDColor.BLACK,
            "1:SYNC": self.LEDColor.BLACK,
            "0:CUE": self.LEDColor.BLACK,
            "0:REV": self.LEDColor.BLACK,
            "1:CUE": self.LEDColor.BLACK,
            "1:REV": self.LEDColor.BLACK,
            "0:LEFT": self.LEDColor.BLACK,
            "0:RIGHT": self.LEDColor.BLACK,
            "1:LEFT": self.LEDColor.BLACK,
            "1:RIGHT": self.LEDColor.BLACK,
            "0:H3": self.LEDColor.BLACK,
            "0:H4": self.LEDColor.BLACK,
            "1:H3": self.LEDColor.BLACK,
            "1:H4": self.LEDColor.BLACK,
            "0:H1": self.LEDColor.BLACK,
            "0:H2": self.LEDColor.BLACK,
            "1:H1": self.LEDColor.BLACK,
            "1:H2": self.LEDColor.BLACK,
            "0:FX4_TOGGLE": self.LEDColor.BLACK,
            "1:FX4_TOGGLE": self.LEDColor.BLACK,
            "0:FX3_TOGGLE": self.LEDColor.BLACK,
            "1:FX3_TOGGLE": self.LEDColor.BLACK,
            "0:FX2_TOGGLE": self.LEDColor.BLACK,
            "1:FX2_TOGGLE": self.LEDColor.BLACK,
            "0:FX1_TOGGLE": self.LEDColor.BLACK,
            "1:FX1_TOGGLE": self.LEDColor.BLACK,
            "0:DECKA_L": self.LEDColor.BLACK,
            "0:DECKA_R": self.LEDColor.BLACK,
            "1:DECKA_L": self.LEDColor.BLACK,
            "1:DECKA_R": self.LEDColor.BLACK,
            "1:BACKLIGHT_1": self.LEDColor.BLACK,
            "1:BACKLIGHT_2": self.LEDColor.BLACK,
            "1:BACKLIGHT_3": self.LEDColor.BLACK,
            "1:BACKLIGHT_4": self.LEDColor.BLACK,
            "1:BACKLIGHT_5": self.LEDColor.BLACK,
            "1:BACKLIGHT_6": self.LEDColor.BLACK,
            "0:BACKLIGHT_6": self.LEDColor.BLACK,
            "0:BACKLIGHT_5": self.LEDColor.BLACK,
            "0:BACKLIGHT_4": self.LEDColor.BLACK,
            "0:BACKLIGHT_3": self.LEDColor.BLACK,
            "0:BACKLIGHT_2": self.LEDColor.BLACK,
            "0:BACKLIGHT_1": self.LEDColor.BLACK
        }

    # led coordinates on the device in mm from the top left corner, ( x, y)
    LED_COORDINATES = {
        "2:SHIFT":  ( 65,   210 ),
        "0:LOOP":   ( 15,   210 ),
        "1:LOOP":   ( 115,  210 ),
        "0:PLAY":   ( 20,   350 ),
        "0:SYNC":   ( 45,   350 ),
        "1:PLAY":   ( 85,   350 ),
        "1:SYNC":   ( 110,  350 ),
        "0:CUE":    ( 20,   285),
        "0:REV":    ( 45,   285),
        "1:CUE":    ( 85,   285),
        "1:REV":    ( 110,  285),
        "0:LEFT":   ( 20,   268),
        "0:RIGHT":  ( 45,   268),
        "1:LEFT":   ( 85,   268),
        "1:RIGHT":  ( 110,  268),
        "0:H3":     ( 20,   252),
        "0:H4":     ( 45,   252),
        "1:H3":     ( 85,   252),
        "1:H4":     ( 110,  252),
        "0:H1":     ( 20,   236),
        "0:H2":     ( 45,   236),
        "1:H1":     ( 85,   236),
        "1:H2":     ( 110,   236),
        "0:FX4_TOGGLE": ( 20,   147),
        "1:FX4_TOGGLE": ( 110,  147),
        "0:FX3_TOGGLE": ( 20,   119),
        "1:FX3_TOGGLE": ( 110,  119),
        "0:FX2_TOGGLE": ( 20,   92),
        "1:FX2_TOGGLE": ( 110,  92),
        "0:FX1_TOGGLE": ( 20,   64),
        "1:FX1_TOGGLE": ( 110,  64),
        "0:DECKA_L":    ( 13, 13),
        "0:DECKA_R":    ( 25, 13),
        "1:DECKA_L":    ( 103, 13),
        "1:DECKA_R":    ( 114, 13),
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
        "0:BACKLIGHT_1": ( 32, 262)
    }

    # screen center point coordinates on the device in mm from the top left corner, ( x, y)
    SCREEN_COORDINATES = {
        "0": ( 23,   34 ),
        "1": ( 64,   34 ),
        "2": ( 117,  34 ),
        "3": ( 45,   187 ),
        "4": ( 84,   187 )
    }

    # screen size ( x, y)
    SCREEN_SIZES = {
        "0": ( 21, 10 ),
        "1": ( 21, 10 ),
        "2": ( 21, 10 ),
        "3": ( 21, 10 ),
        "4": ( 21, 10 )
    }

    def _decode_button_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        if e:=self._decode_bit_byte("2:SHIFT", 1, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:PLAY", 1, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:SYNC", 1, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:PLAY", 1, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:SYNC", 1, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:CUE", 1, 5, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:REV", 1, 6, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:CUE", 1, 7, current_report): events.append(e)

        if e:=self._decode_bit_byte("1:REV", 2, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:LEFT", 2, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:RIGHT", 2, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:LEFT", 2, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:RIGHT", 2, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:H3", 2, 5, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:H4", 2, 6, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:H3", 2, 7, current_report): events.append(e)

        if e:=self._decode_bit_byte("1:H4", 3, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:H1", 3, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:H2", 3, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:H1", 3, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:H2", 3, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:FX4_TOGGLE", 3, 5, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:FX4_TOGGLE", 3, 6, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:FX3_TOGGLE", 3, 7, current_report): events.append(e)

        if e:=self._decode_bit_byte("1:FX3_TOGGLE", 4, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:FX2_TOGGLE", 4, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:FX2_TOGGLE", 4, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:FX1_TOGGLE", 4, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:FX1_TOGGLE", 4, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:DECKA_L", 4, 5, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:DECKA_R", 4, 6, current_report): events.append(e)
        if e:=self._decode_bit_byte("2:MODE", 4, 7, current_report): events.append(e)

        if e:=self._decode_bit_byte("1:DECKA_L", 5, 0, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:DECKA_R", 5, 1, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:LOOP", 5, 2, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:LOOP", 5, 3, current_report): events.append(e)
        if e:=self._decode_bit_byte("0:BROWSE", 5, 4, current_report): events.append(e)
        if e:=self._decode_bit_byte("1:BROWSE", 5, 5, current_report): events.append(e)

        return events

    def _decode_encoder_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        encoder = current_report[7] & 0x0F
        encoder_prev = prev[7] & 0x0F
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("0:LOOP:R")
        elif diff > 8:
            events.append("0:LOOP:L")

        encoder = (current_report[7] & 0xF0) >> 4
        encoder_prev = (prev[7] & 0xF0) >> 4
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("1:LOOP:R")
        elif diff > 8:
            events.append("1:LOOP:L")

        encoder = current_report[8] & 0x0F
        encoder_prev = prev[8] & 0x0F
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("0:BROWSE:R")
        elif diff > 8:
            events.append("0:BROWSE:L")

        encoder = (current_report[8] & 0xF0) >> 4
        encoder_prev = (prev[8] & 0xF0) >> 4
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("1:BROWSE:R")
        elif diff > 8:
            events.append("1:BROWSE:L")

        return events

    def _decode_poti_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        value = (current_report[10] << 8) | current_report[9]
        prev_value = (prev[10] << 8) | prev[9]
        if value != prev_value:
            events.append(f"0:FX4:{value}")

        value = (current_report[12] << 8) | current_report[11]
        prev_value = (prev[12] << 8) | prev[11]
        if value != prev_value:
            events.append(f"1:FX4:{value}")

        value = (current_report[14] << 8) | current_report[13]
        prev_value = (prev[14] << 8) | prev[13]
        if value != prev_value:
            events.append(f"0:FX3:{value}")

        value = (current_report[16] << 8) | current_report[15]
        prev_value = (prev[16] << 8) | prev[15]
        if value != prev_value:
            events.append(f"1:FX3:{value}")

        value = (current_report[18] << 8) | current_report[17]
        prev_value = (prev[18] << 8) | prev[17]
        if value != prev_value:
            events.append(f"0:FX2:{value}")

        value = (current_report[20] << 8) | current_report[19]
        prev_value = (prev[20] << 8) | prev[19]
        if value != prev_value:
            events.append(f"1:FX2:{value}")

        value = (current_report[22] << 8) | current_report[21]
        prev_value = (prev[22] << 8) | prev[21]
        if value != prev_value:
            events.append(f"0:FX1:{value}")

        value = (current_report[24] << 8) | current_report[23]
        prev_value = (prev[24] << 8) | prev[23]
        if value != prev_value:
            events.append(f"1:FX1:{value}")

        return events

    def decode_events(self, current_report):
        events = []

        if self._get_previous_report(current_report) is None:
            self._set_previous_report(current_report)
            return []

        if current_report == self._get_previous_report(current_report):
            return []

        events.extend(self._decode_button_events(current_report))
        events.extend(self._decode_encoder_events(current_report))
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
        report_bytes.insert(34, 0x7C)
        report_bytes.insert(43, 0x02)

        report_bytes = bytes(report_bytes)
        if report_bytes:
            self.send_queue.put(report_bytes)