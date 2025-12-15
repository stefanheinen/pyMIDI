from .native_instruments_hid_device import Native_Instruments_HID_Device

class HIDDevice(Native_Instruments_HID_Device):
    # Native Instruments X1 MK3
    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x2200
    PACKET_SIZE = 64
    DEVICE_NAME = "TRAKTOR X1 MK3"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 5

    def __init__(self):
        super().__init__()

        self.previousReport = None

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

    def decode_button_events(self, cur):
        events = []

        if e:=self.decode_bit_byte("2:SHIFT", 0, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("0:PLAY", 0, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("0:SYNC", 0, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("1:PLAY", 0, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("1:SYNC", 0, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("0:CUE", 0, 5, cur): events.append(e)
        if e:=self.decode_bit_byte("0:REV", 0, 6, cur): events.append(e)
        if e:=self.decode_bit_byte("1:CUE", 0, 7, cur): events.append(e)

        if e:=self.decode_bit_byte("1:REV", 1, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("0:LEFT", 1, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("0:RIGHT", 1, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("1:LEFT", 1, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("1:RIGHT", 1, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("0:H3", 1, 5, cur): events.append(e)
        if e:=self.decode_bit_byte("0:H4", 1, 6, cur): events.append(e)
        if e:=self.decode_bit_byte("1:H3", 1, 7, cur): events.append(e)

        if e:=self.decode_bit_byte("1:H4", 2, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("0:H1", 2, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("0:H2", 2, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("1:H1", 2, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("1:H2", 2, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("0:FX4_TOGGLE", 2, 5, cur): events.append(e)
        if e:=self.decode_bit_byte("1:FX4_TOGGLE", 2, 6, cur): events.append(e)
        if e:=self.decode_bit_byte("0:FX3_TOGGLE", 2, 7, cur): events.append(e)

        if e:=self.decode_bit_byte("1:FX3_TOGGLE", 3, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("0:FX2_TOGGLE", 3, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("1:FX2_TOGGLE", 3, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("0:FX1_TOGGLE", 3, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("1:FX1_TOGGLE", 3, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("0:DECKA_L", 3, 5, cur): events.append(e)
        if e:=self.decode_bit_byte("0:DECKA_R", 3, 6, cur): events.append(e)
        if e:=self.decode_bit_byte("2:MODE", 3, 7, cur): events.append(e)

        if e:=self.decode_bit_byte("1:DECKA_L", 4, 0, cur): events.append(e)
        if e:=self.decode_bit_byte("1:DECKA_R", 4, 1, cur): events.append(e)
        if e:=self.decode_bit_byte("0:LOOP", 4, 2, cur): events.append(e)
        if e:=self.decode_bit_byte("1:LOOP", 4, 3, cur): events.append(e)
        if e:=self.decode_bit_byte("0:BROWSE", 4, 4, cur): events.append(e)
        if e:=self.decode_bit_byte("1:BROWSE", 4, 5, cur): events.append(e)

        return events

    def decode_encoder_events(self, current):
        events = []
        prev = self.previousReport

        encoder = current[6] & 0x0F
        encoder_prev = prev[6] & 0x0F
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("0:LOOP:R")
        elif diff > 8:
            events.append("0:LOOP:L")

        encoder = (current[6] & 0xF0) >> 4
        encoder_prev = (prev[6] & 0xF0) >> 4
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("1:LOOP:R")
        elif diff > 8:
            events.append("1:LOOP:L")

        encoder = current[7] & 0x0F
        encoder_prev = prev[7] & 0x0F
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("0:BROWSE:R")
        elif diff > 8:
            events.append("0:BROWSE:L")

        encoder = (current[7] & 0xF0) >> 4
        encoder_prev = (prev[7] & 0xF0) >> 4
        diff = (encoder - encoder_prev) % 16
        if 0 < diff < 9:
            events.append("1:BROWSE:R")
        elif diff > 8:
            events.append("1:BROWSE:L")

        return events

    def decode_poti_events(self, current):
        events = []
        prev = self.previousReport

        value = (current[9] << 8) | current[8]
        prev_value = (prev[9] << 8) | prev[8]
        if value != prev_value:
            events.append(f"0:FX4:{value}")

        value = (current[11] << 8) | current[10]
        prev_value = (prev[11] << 8) | prev[10]
        if value != prev_value:
            events.append(f"1:FX4:{value}")

        value = (current[13] << 8) | current[12]
        prev_value = (prev[13] << 8) | prev[12]
        if value != prev_value:
            events.append(f"0:FX3:{value}")

        value = (current[15] << 8) | current[14]
        prev_value = (prev[15] << 8) | prev[14]
        if value != prev_value:
            events.append(f"1:FX3:{value}")

        value = (current[17] << 8) | current[16]
        prev_value = (prev[17] << 8) | prev[16]
        if value != prev_value:
            events.append(f"0:FX2:{value}")

        value = (current[19] << 8) | current[18]
        prev_value = (prev[19] << 8) | prev[18]
        if value != prev_value:
            events.append(f"1:FX2:{value}")

        value = (current[21] << 8) | current[20]
        prev_value = (prev[21] << 8) | prev[20]
        if value != prev_value:
            events.append(f"0:FX1:{value}")

        value = (current[23] << 8) | current[22]
        prev_value = (prev[23] << 8) | prev[22]
        if value != prev_value:
            events.append(f"1:FX1:{value}")

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
        events.extend(self.decode_encoder_events(current))
        events.extend(self.decode_poti_events(current))

        self.previousReport = current

        # if the event has not been mapped, print the raw hid report to help with mapping
        if not events:
            print(list(current))

        return events

    def flush_leds(self):
        report_bytes = list(self.LED_bytes.values())
        report_bytes.insert(0, 0x80)
        report_bytes.insert(34, 0x7C)
        report_bytes.insert(43, 0x02)

        report_bytes = bytes(report_bytes)
        if report_bytes:
            self.send_queue.put(report_bytes)

# def read_packets():
#     import xml.etree.ElementTree as ET
#     import pathlib
#
#     packet_path = pathlib.Path.home() / "TMP" / "z1_get_first_state.pdml"
#
#     tree = ET.parse(packet_path)
#     root = tree.getroot()
#
#     for pkt in root.findall(".//packet"):
#         data_bytes = []
#         for field in pkt.findall(".//field[@name='usbhid.data']"):
#             hex_str = field.attrib.get('show')
#             if hex_str:
#                 data_bytes = hex_str.split(":")
#         if data_bytes:
#             yield(data_bytes)


# def main():
    #
    # print("Manufacturer: ", h.manufacturer)
    # print("Product:      ", h.product)
    # print("Serial no.:   ", h.serial)
    #
    # print("\nReading HID reports (Ctrl+C to stop)...\n")
    #
    # try:
    #     while True:
    #         b = X1.read()
    #
    #         if b:
    #             events = X1.decode_events(b[1:])
    #             print(events)
    #         else:
    #             time.sleep(0.01)
    #
    #
    # except KeyboardInterrupt:
    #     print("\nInterrupted, closing device.")
    # finally:
    #     h.close()