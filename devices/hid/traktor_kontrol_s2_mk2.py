import time
from enum import IntEnum
from logging import debug
from typing import List

from .native_instruments_hid_device import Native_Instruments_HID_Device

class HIDDevice(Native_Instruments_HID_Device):
    # Native Instruments Traktor Kontrol S2 Mk 2
    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x1320
    PACKET_SIZE = 64
    DEVICE_NAME = "TRAKTOR KONTROL S2 MK2"

    def __init__(self):
        super().__init__()

        self._previousReport = [None, None]

        self.LED_bytes = {
            "0:M1": self.LEDColor.BLACK,
            "0:M2": self.LEDColor.BLACK,
            "0:M3": self.LEDColor.BLACK,
            "0:M4": self.LEDColor.BLACK,
            "0:M5": self.LEDColor.BLACK,
            "1:M1": self.LEDColor.BLACK,
            "1:M2": self.LEDColor.BLACK,
            "1:M3": self.LEDColor.BLACK,
            "1:M4": self.LEDColor.BLACK,
            "1:M5": self.LEDColor.BLACK,
            "0:DRYWET_TOGGLE": self.LEDColor.BLACK,
            "0:FX1_TOGGLE": self.LEDColor.BLACK,
            "0:FX2_TOGGLE": self.LEDColor.BLACK,
            "0:FX3_TOGGLE": self.LEDColor.BLACK,
            "0:DECKA_L": self.LEDColor.BLACK,
            "0:DECKA_R": self.LEDColor.BLACK,
            "1:DECKA_L": self.LEDColor.BLACK,
            "1:DECKA_R": self.LEDColor.BLACK,
            "1:DRYWET_TOGGLE": self.LEDColor.BLACK,
            "1:FX1_TOGGLE": self.LEDColor.BLACK,
            "1:FX2_TOGGLE": self.LEDColor.BLACK,
            "1:FX3_TOGGLE": self.LEDColor.BLACK,
            "2:REMIX_A": self.LEDColor.BLACK,
            "2:REMIX_B": self.LEDColor.BLACK,
            "2:LOAD_A": self.LEDColor.BLACK,
            "2:LOAD_B": self.LEDColor.BLACK,
            "0:HEADPHONE_CUE": self.LEDColor.BLACK,
            "2:EXCLAMATION_MARK": self.LEDColor.BLACK,
            "2:USB": self.LEDColor.BLACK,
            "3:UNKNOWN": self.LEDColor.BLACK,
            "1:HEADPHONE_CUE": self.LEDColor.BLACK,
            "0:FLUX": self.LEDColor.BLACK,
            "0:LOOP_IN": self.LEDColor.BLACK,
            "0:LOOP_OUT": self.LEDColor.BLACK,
            "1:LOOP_IN": self.LEDColor.BLACK,
            "1:LOOP_OUT": self.LEDColor.BLACK,
            "1:FLUX": self.LEDColor.BLACK,
            "0:H1:R": self.LEDColor.BLACK,
            "0:H1:G": self.LEDColor.BLACK,
            "0:H1:B": self.LEDColor.BLACK,
            "0:H2:R": self.LEDColor.BLACK,
            "0:H2:G": self.LEDColor.BLACK,
            "0:H2:B": self.LEDColor.BLACK,
            "0:H3:R": self.LEDColor.BLACK,
            "0:H3:G": self.LEDColor.BLACK,
            "0:H3:B": self.LEDColor.BLACK,
            "0:H4:R": self.LEDColor.BLACK,
            "0:H4:G": self.LEDColor.BLACK,
            "0:H4:B": self.LEDColor.BLACK,
            "1:H1:R": self.LEDColor.BLACK,
            "1:H1:G": self.LEDColor.BLACK,
            "1:H1:B": self.LEDColor.BLACK,
            "1:H2:R": self.LEDColor.BLACK,
            "1:H2:G": self.LEDColor.BLACK,
            "1:H2:B": self.LEDColor.BLACK,
            "1:H3:R": self.LEDColor.BLACK,
            "1:H3:G": self.LEDColor.BLACK,
            "1:H3:B": self.LEDColor.BLACK,
            "1:H4:R": self.LEDColor.BLACK,
            "1:H4:G": self.LEDColor.BLACK,
            "1:H4:B": self.LEDColor.BLACK,
            "0:SHIFT": self.LEDColor.BLACK,
            "0:SYNC": self.LEDColor.BLACK,
            "0:CUE": self.LEDColor.BLACK,
            "0:PLAY": self.LEDColor.BLACK,
            "1:SHIFT": self.LEDColor.BLACK,
            "1:SYNC": self.LEDColor.BLACK,
            "1:CUE": self.LEDColor.BLACK,
            "1:PLAY": self.LEDColor.BLACK,
        }

    class LEDColor(IntEnum):
        BLACK = 0x00
        L0 = 0x00
        L1 = 0x10
        L2 = 0x20
        L3 = 0x30
        L4 = 0x40
        L5 = 0x50
        L6 = 0x60
        L7 = 0x70
        L8 = 0x80
        L9 = 0x90
        L10 = 0xA0
        L11 = 0xB0
        L12 = 0xC0
        L13 = 0xD0
        L14 = 0xE0
        L15 = 0xF0
        WHITE = 0xFF

    # led coordinates on the device in mm from the top left corner, ( x, y)
    LED_COORDINATES = {
        # "2:SHIFT":  ( 65,   210 ),
        # "0:LOOP":   ( 15,   210 ),
        # "1:LOOP":   ( 115,  210 ),
        # "0:PLAY":   ( 20,   350 ),
        # "0:SYNC":   ( 45,   350 ),
        # "1:PLAY":   ( 85,   350 ),
        # "1:SYNC":   ( 110,  350 ),
        # "0:CUE":    ( 20,   285),
        # "0:REV":    ( 45,   285),
        # "1:CUE":    ( 85,   285),
        # "1:REV":    ( 110,  285),
        # "0:LEFT":   ( 20,   268),
        # "0:RIGHT":  ( 45,   268),
        # "1:LEFT":   ( 85,   268),
        # "1:RIGHT":  ( 110,  268),
        # "0:H3":     ( 20,   252),
        # "0:H4":     ( 45,   252),
        # "1:H3":     ( 85,   252),
        # "1:H4":     ( 110,  252),
        # "0:H1":     ( 20,   236),
        # "0:H2":     ( 45,   236),
        # "1:H1":     ( 85,   236),
        # "1:H2":     ( 110,   236),
        # "0:FX4_TOGGLE": ( 20,   147),
        # "1:FX4_TOGGLE": ( 110,  147),
        # "0:FX3_TOGGLE": ( 20,   119),
        # "1:FX3_TOGGLE": ( 110,  119),
        # "0:FX2_TOGGLE": ( 20,   92),
        # "1:FX2_TOGGLE": ( 110,  92),
        # "0:FX1_TOGGLE": ( 20,   64),
        # "1:FX1_TOGGLE": ( 110,  64),
        # "0:DECKA_L":    ( 13, 13),
        # "0:DECKA_R":    ( 25, 13),
        # "1:DECKA_L":    ( 103, 13),
        # "1:DECKA_R":    ( 114, 13),
        # "1:BACKLIGHT_1": ( 94, 262),
        # "1:BACKLIGHT_2": ( 94, 229),
        # "1:BACKLIGHT_3": ( 94, 195),
        # "1:BACKLIGHT_4": ( 94, 164),
        # "1:BACKLIGHT_5": ( 94, 129),
        # "1:BACKLIGHT_6": ( 94, 96),
        # "0:BACKLIGHT_6": ( 32, 96),
        # "0:BACKLIGHT_5": ( 32, 129),
        # "0:BACKLIGHT_4": ( 32, 164),
        # "0:BACKLIGHT_3": ( 32, 195),
        # "0:BACKLIGHT_2": ( 32, 229),
        # "0:BACKLIGHT_1": ( 32, 262)
    }

    def _decode_button_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        if current_report[0] == 1:
            # Left Deck
            if e:=self._decode_bit_byte("0:SHIFT", 11, 3, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:SYNC", 11, 2, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:CUE", 11, 1, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:PLAY", 11, 0, current_report): events.append(e)

            if e:=self._decode_bit_byte("0:H1", 11, 7, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:H2", 11, 6, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:H3", 11, 5, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:H4", 11, 4, current_report): events.append(e)

            if e:=self._decode_bit_byte("0:LOOP_IN", 12, 6, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:LOOP_OUT", 12, 7, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:LOOP_MOVE", 15, 0, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:LOOP_SIZE", 15, 1, current_report): events.append(e)

            if e := self._decode_bit_byte("0:FLUX", 12, 5, current_report): events.append(e)

            if e := self._decode_bit_byte("0:DRYWET_TOGGLE", 14, 4, current_report): events.append(e)
            if e := self._decode_bit_byte("0:FX1_TOGGLE", 14, 7, current_report): events.append(e)
            if e := self._decode_bit_byte("0:FX2_TOGGLE", 14, 6, current_report): events.append(e)
            if e := self._decode_bit_byte("0:FX3_TOGGLE", 14, 5, current_report): events.append(e)

            if e := self._decode_bit_byte("0:GAIN", 13, 6, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:DECKA_L", 14, 3, current_report): events.append(e)
            if e:=self._decode_bit_byte("0:DECKA_R", 14, 2, current_report): events.append(e)

            if e:=self._decode_bit_byte("0:HEADPHONE_CUE", 12, 4, current_report): events.append(e)

            if e:=self._decode_bit_byte("0:JOG", 10, 0, current_report): events.append(e)


            # Right Deck
            if e:=self._decode_bit_byte("1:SHIFT", 9, 3, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:SYNC", 9, 2, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:CUE", 9, 1, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:PLAY", 9, 0, current_report): events.append(e)
            
            if e:=self._decode_bit_byte("1:H1", 9, 7, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:H2", 9, 6, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:H3", 9, 5, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:H4", 9, 4, current_report): events.append(e)

            if e:=self._decode_bit_byte("1:LOOP_IN", 10, 6, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:LOOP_OUT", 10, 7, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:LOOP_MOVE", 15, 3, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:LOOP_SIZE", 15, 4, current_report): events.append(e)

            if e := self._decode_bit_byte("1:FLUX", 10, 5, current_report): events.append(e)

            if e := self._decode_bit_byte("1:DRYWET_TOGGLE", 13, 2, current_report): events.append(e)
            if e := self._decode_bit_byte("1:FX1_TOGGLE", 13, 5, current_report): events.append(e)
            if e := self._decode_bit_byte("1:FX2_TOGGLE", 13, 4, current_report): events.append(e)
            if e := self._decode_bit_byte("1:FX3_TOGGLE", 13, 3, current_report): events.append(e)

            if e := self._decode_bit_byte("0:GAIN", 13, 7, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:DECKA_L", 14, 1, current_report): events.append(e)
            if e:=self._decode_bit_byte("1:DECKA_R", 14, 0, current_report): events.append(e)

            if e:=self._decode_bit_byte("1:HEADPHONE_CUE", 10, 4, current_report): events.append(e)

            if e:=self._decode_bit_byte("1:JOG", 10, 1, current_report): events.append(e)


            # Center Channel
            if e := self._decode_bit_byte("2:BROWSE", 15, 2, current_report): events.append(e)
            if e := self._decode_bit_byte("2:LOAD_A", 12, 3, current_report): events.append(e)
            if e := self._decode_bit_byte("2:LOAD_B", 12, 2, current_report): events.append(e)

            if e := self._decode_bit_byte("2:REMIX_A", 12, 1, current_report): events.append(e)
            if e := self._decode_bit_byte("2:REMIX_B", 12, 0, current_report): events.append(e)

            if e := self._decode_bit_byte("2:OUTPUT_SELECT", 10, 2, current_report): events.append(e)

            if e := self._decode_bit_byte("2:MIC_ENGAGE", 10, 3, current_report): events.append(e)
        return events

    def _decode_encoder_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        if current_report[0] == 1:
            # Left Deck
            encoder = current_report[1]
            encoder_prev = prev[1]
            diff = (encoder - encoder_prev) % 256
            if diff == 0:
                pass
            if 0 < diff < 129:
                events.append("0:JOG:R")
            elif diff > 128:
                events.append("0:JOG:L")

            # Right Deck
            encoder = current_report[5]
            encoder_prev = prev[5]
            diff = (encoder - encoder_prev) % 256
            if 0 < diff < 129:
                events.append("1:JOG:R")
            elif diff > 128:
                events.append("1:JOG:L")
        elif current_report[0] == 2:
            # Left Deck
            encoder = (current_report[3] & 0xF0) >> 4
            encoder_prev = (prev[3] & 0xF0) >> 4
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("0:GAIN:R")
            elif diff > 8:
                events.append("0:GAIN:L")

            encoder = current_report[1] & 0x0F
            encoder_prev = prev[1] & 0x0F
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("0:LOOP_MOVE:R")
            elif diff > 8:
                events.append("0:LOOP_MOVE:L")

            encoder = (current_report[1] & 0xF0) >> 4
            encoder_prev = (prev[1] & 0xF0) >> 4
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("0:LOOP_SIZE:R")
            elif diff > 8:
                events.append("0:LOOP_SIZE:L")

            # Right Deck
            encoder = current_report[4] & 0x0F
            encoder_prev = prev[4] & 0x0F
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("1:GAIN:R")
            elif diff > 8:
                events.append("1:GAIN:L")

            encoder = current_report[3] & 0x0F
            encoder_prev = prev[3] & 0x0F
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("1:LOOP_SIZE:R")
            elif diff > 8:
                events.append("1:LOOP_SIZE:L")

            encoder = (current_report[2] & 0xF0) >> 4
            encoder_prev = (prev[2] & 0xF0) >> 4
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("1:LOOP_MOVE:R")
            elif diff > 8:
                events.append("1:LOOP_MOVE:L")

            # Center Channel
            encoder = current_report[2] & 0x0F
            encoder_prev = prev[2] & 0x0F
            diff = (encoder - encoder_prev) % 16
            if 0 < diff < 9:
                events.append("2:BROWSE:R")
            elif diff > 8:
                events.append("2:BROWSE:L")

        return events

    def _decode_poti_events(self, current_report):
        events = []
        prev = self._get_previous_report(current_report)

        if not prev:
            return []

        if current_report[0] == 2:
            # Left Deck
            value = (current_report[24] << 8) | current_report[23]
            prev_value = (prev[24] << 8) | prev[23]
            if value != prev_value:
                events.append(f"0:DRY_WET:{value}")

            value = (current_report[26] << 8) | current_report[25]
            prev_value = (prev[26] << 8) | prev[25]
            if value != prev_value:
                events.append(f"0:FX1:{value}")

            value = (current_report[28] << 8) | current_report[27]
            prev_value = (prev[28] << 8) | prev[27]
            if value != prev_value:
                events.append(f"0:FX2:{value}")

            value = (current_report[30] << 8) | current_report[29]
            prev_value = (prev[30] << 8) | prev[29]
            if value != prev_value:
                events.append(f"0:FX3:{value}")

            value = (current_report[8] << 8) | current_report[7]
            prev_value = (prev[8] << 8) | prev[7]
            if value != prev_value:
                events.append(f"0:TEMPO:{value}")

            value = (current_report[40] << 8) | current_report[39]
            prev_value = (prev[40] << 8) | prev[39]
            if value != prev_value:
                events.append(f"0:HI:{value}")

            value = (current_report[42] << 8) | current_report[41]
            prev_value = (prev[42] << 8) | prev[41]
            if value != prev_value:
                events.append(f"0:MID:{value}")

            value = (current_report[44] << 8) | current_report[43]
            prev_value = (prev[44] << 8) | prev[43]
            if value != prev_value:
                events.append(f"0:LOW:{value}")

            value = (current_report[20] << 8) | current_report[19]
            prev_value = (prev[20] << 8) | prev[19]
            if value != prev_value:
                events.append(f"0:FADER:{value}")
                
            
            # Right Deck
            value = (current_report[32] << 8) | current_report[31]
            prev_value = (prev[32] << 8) | prev[31]
            if value != prev_value:
                events.append(f"1:DRY_WET:{value}")

            value = (current_report[34] << 8) | current_report[33]
            prev_value = (prev[34] << 8) | prev[33]
            if value != prev_value:
                events.append(f"1:FX1:{value}")

            value = (current_report[36] << 8) | current_report[35]
            prev_value = (prev[36] << 8) | prev[35]
            if value != prev_value:
                events.append(f"1:FX2:{value}")

            value = (current_report[38] << 8) | current_report[37]
            prev_value = (prev[38] << 8) | prev[37]
            if value != prev_value:
                events.append(f"1:FX3:{value}")

            value = (current_report[10] << 8) | current_report[9]
            prev_value = (prev[10] << 8) | prev[9]
            if value != prev_value:
                events.append(f"1:TEMPO:{value}")

            value = (current_report[46] << 8) | current_report[45]
            prev_value = (prev[46] << 8) | prev[45]
            if value != prev_value:
                events.append(f"1:HI:{value}")

            value = (current_report[48] << 8) | current_report[47]
            prev_value = (prev[48] << 8) | prev[47]
            if value != prev_value:
                events.append(f"1:MID:{value}")

            value = (current_report[50] << 8) | current_report[49]
            prev_value = (prev[50] << 8) | prev[49]
            if value != prev_value:
                events.append(f"1:LOW:{value}")

            value = (current_report[22] << 8) | current_report[21]
            prev_value = (prev[22] << 8) | prev[21]
            if value != prev_value:
                events.append(f"1:FADER:{value}")


            # Center Channel
            value = (current_report[14] << 8) | current_report[13]
            prev_value = (prev[14] << 8) | prev[13]
            if value != prev_value:
                events.append(f"2:REMIX:{value}")

            value = (current_report[6] << 8) | current_report[5]
            prev_value = (prev[6] << 8) | prev[5]
            if value != prev_value:
                events.append(f"2:CROSSFADER:{value}")

            value = (current_report[16] << 8) | current_report[15]
            prev_value = (prev[16] << 8) | prev[15]
            if value != prev_value:
                events.append(f"2:MAIN:{value}")

            value = (current_report[12] << 8) | current_report[11]
            prev_value = (prev[12] << 8) | prev[11]
            if value != prev_value:
                events.append(f"2:HEADPHONE_MIX:{value}")

            value = (current_report[18] << 8) | current_report[17]
            prev_value = (prev[18] << 8) | prev[17]
            if value != prev_value:
                events.append(f"2:OUTPUT_LEVEL:{value}")

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
        if not (self.LED_bytes == self._last_led_bytes):
            report_bytes = list(self.LED_bytes.values())[0:37]
            report_bytes.insert(0, 0x80)
            self.send_queue.put(bytes(report_bytes))

            report_bytes = list(self.LED_bytes.values())[37:]
            report_bytes.insert(0, 0x81)
            self.send_queue.put(bytes(report_bytes))

            self._last_led_bytes = self.LED_bytes.copy()

    def _request_control_status_connected_device(self) -> List[bytes]:
        reports = [self.hid_device.get_input_report(1, self.PACKET_SIZE),
                   self.hid_device.get_input_report(2, self.PACKET_SIZE)]
        return reports

    def mixer_leds_from_value(self, channel, fader_value: int):
        # led_level = int(int(fader_value) * 11 / 4095)
        #
        # channel = int(channel)
        #
        # for l in range(0, 10):
        #     current_key, current_value = list(self.LED_bytes.items())[channel * 10 + l]
        #
        #     if led_level > l:
        #         if current_value == True:
        #             pass
        #         else:
        #             self.LED_bytes[current_key] = self.LEDColor.WHITE
        #     else:
        #         if current_value == False:
        #             pass
        #         else:
        #             self.LED_bytes[current_key] = self.LEDColor.BLACK
        #
        # self.flush_leds()
        pass

    def mixer_leds_from_fader(self):
        # prev = self._get_previous_report(bytes([1]))
        # if prev:
        #     value0 = (prev[29] << 8) | prev[28]
        #     value1 = (prev[31] << 8) | prev[30]
        #     self.mixer_leds_from_value(0, value0)
        #     self.mixer_leds_from_value(1, value1)
        pass
