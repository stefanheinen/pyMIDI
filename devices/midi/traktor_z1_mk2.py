import time

import mido

from .midi_device import MIDIEvent, MIDI_Device

class Device(MIDI_Device):
    MIDI_port_name = "Traktor Z1 MK2"
    DEVICE_NAME = "TRAKTOR Z1 MK2"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 3

    def __init__(self):
        super().__init__()
        self.mixer_led_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.fader_values = [0,0,0]
        pass

    def decode_events(self, msg:mido.messages.messages) -> []:
        ### FX1 ###
        if MIDIEvent(channel=2, note=0, velocity=127) == msg: return [f"2:FX1_BUTTON:D"]  # down
        if MIDIEvent(channel=2, note=0, velocity=0) == msg: return [f"2:FX1_BUTTON:U"]  # up

        ### FX2 ###
        if MIDIEvent(channel=2, note=1, velocity=127) == msg: return [f"2:FX2_BUTTON:D"]  # down
        if MIDIEvent(channel=2, note=1, velocity=0) == msg: return [f"2:FX2_BUTTON:U"]  # up

        ### FX3 ###
        if MIDIEvent(channel=2, note=2, velocity=127) == msg: return [f"2:FX3_BUTTON:D"]  # down
        if MIDIEvent(channel=2, note=2, velocity=0) == msg: return [f"2:FX3_BUTTON:U"]  # up

        ### FX4 ###
        if MIDIEvent(channel=2, note=3, velocity=127) == msg: return [f"2:FX4_BUTTON:D"]  # down
        if MIDIEvent(channel=2, note=3, velocity=0) == msg: return [f"2:FX4_BUTTON:U"]  # up

        ### - ###
        if MIDIEvent(channel=2, note=4, velocity=127) == msg: return [f"2:-:D"]  # down
        if MIDIEvent(channel=2, note=4, velocity=0) == msg: return [f"2:-:U"]  # up

        ### HEADPHONE_L ###
        if MIDIEvent(channel=2, note=5, velocity=127) == msg: return [f"2:HEADPHONE_L:D"]  # down
        if MIDIEvent(channel=2, note=5, velocity=0) == msg: return [f"2:HEADPHONE_L:U"]  # up

        ### HEADPHONE_R ###
        if MIDIEvent(channel=2, note=6, velocity=127) == msg: return [f"2:HEADPHONE_R:D"]  # down
        if MIDIEvent(channel=2, note=6, velocity=0) == msg: return [f"2:HEADPHONE_R:U"]  # up

        ### MFX ###
        if MIDIEvent(note=2, velocity=127) == msg: return [f"{msg.channel}:FX_TOGGLE:D"]  # down
        if MIDIEvent(note=2, velocity=0) == msg: return [f"{msg.channel}:FX_TOGGLE:U"]  # up

        ### MODE_MIX ###
        if MIDIEvent(note=0, velocity=127) == msg: return [f"{msg.channel}:MODE_MIX:D"]  # down
        if MIDIEvent(note=0, velocity=0) == msg: return [f"{msg.channel}:MODE_MIX:U"]  # up

        ### MODE_STEMS ###
        if MIDIEvent(note=1, velocity=127) == msg: return [f"{msg.channel}:MODE_STEMS:D"]  # down
        if MIDIEvent(note=1, velocity=0) == msg: return [f"{msg.channel}:MODE_STEMS:U"]  # up

        ### FADER ###
        if MIDIEvent(control=21) == msg:
            self.fader_values[msg.channel] = msg.value
            return [f"{msg.channel}:FADER:{msg.value}"]

        ### MAIN VOLUME ###
        if MIDIEvent(channel=2, control=16) == msg: return [f"{msg.channel}:MAIN:{msg.value}"]

        ### HEADPHONE MIX ###
        if MIDIEvent(channel=2, control=17) == msg: return [f"{msg.channel}:HP_MIX:{msg.value}"]

        ### HEADPHONE VOL ###
        if MIDIEvent(channel=2, control=18) == msg: return [f"{msg.channel}:HP_VOL:{msg.value}"]

        ### GAIN ###
        if MIDIEvent(control=16) == msg: return [ f"{msg.channel}:GAIN:{msg.value}"]

        ### HI ###
        if MIDIEvent(control=17) == msg: return [ f"{msg.channel}:HI:{msg.value}"]

        ### MID ###
        if MIDIEvent(control=18) == msg: return [ f"{msg.channel}:MID:{msg.value}"]

        ### LOW ###
        if MIDIEvent(control=19) == msg: return [ f"{msg.channel}:LOW:{msg.value}"]

        ### FX ###
        if MIDIEvent(control=20) == msg: return [ f"{msg.channel}:FX:{msg.value}"]

        return None

    def set_led(self, led_name: str, color):
        channel, led = led_name.split(":", 1)

        channel = int(channel)

        if color:
            velocity = 127
        else:
            velocity = 0

        if led == "MODE_MIX" or led == "0": self.send_queue.put(mido.Message('note_on', channel=channel, note=0, velocity=velocity))
        if led == "MODE_STEMS" or led == "1": self.send_queue.put(mido.Message('note_on', channel=channel, note=1, velocity=velocity))

        if led == "FX1_BUTTON" or led == "2": self.send_queue.put(mido.Message('note_on', channel=2, note=0, velocity=velocity))
        if led == "FX2_BUTTON" or led == "3": self.send_queue.put(mido.Message('note_on', channel=2, note=1, velocity=velocity))
        if led == "FX3_BUTTON" or led == "4": self.send_queue.put(mido.Message('note_on', channel=2, note=2, velocity=velocity))
        if led == "FX4_BUTTON" or led == "5": self.send_queue.put(mido.Message('note_on', channel=2, note=3, velocity=velocity))
        if led == "-" or led == "6": self.send_queue.put(mido.Message('note_on', channel=2, note=4, velocity=velocity))

        if led == "FX_TOGGLE" or led == "7": self.send_queue.put(mido.Message('note_on', channel=channel, note=2, velocity=velocity))

        if led == "HEADPHONE_L" or led == "8": self.send_queue.put(mido.Message('note_on', channel=2, note=5, velocity=velocity))
        if led == "HEADPHONE_R" or led == "9": self.send_queue.put(mido.Message('note_on', channel=2, note=6, velocity=velocity))

        if led == "M1" or led == "19": self.send_queue.put(mido.Message('note_on', channel=channel, note=10, velocity=velocity))
        if led == "M2" or led == "18": self.send_queue.put(mido.Message('note_on', channel=channel, note=11, velocity=velocity))
        if led == "M3" or led == "17": self.send_queue.put(mido.Message('note_on', channel=channel, note=12, velocity=velocity))
        if led == "M4" or led == "16": self.send_queue.put(mido.Message('note_on', channel=channel, note=13, velocity=velocity))
        if led == "M5" or led == "15": self.send_queue.put(mido.Message('note_on', channel=channel, note=14, velocity=velocity))
        if led == "M6" or led == "14": self.send_queue.put(mido.Message('note_on', channel=channel, note=15, velocity=velocity))
        if led == "M7" or led == "13": self.send_queue.put(mido.Message('note_on', channel=channel, note=16, velocity=velocity))
        if led == "M8" or led == "12": self.send_queue.put(mido.Message('note_on', channel=channel, note=17, velocity=velocity))
        if led == "M9" or led == "11": self.send_queue.put(mido.Message('note_on', channel=channel, note=18, velocity=velocity))
        if led == "M10" or led == "10": self.send_queue.put(mido.Message('note_on', channel=channel, note=19, velocity=velocity))


    def mixer_leds_from_value(self, channel, fader_value: int):
        led_level = int(int(fader_value) * 11 / 127)

        channel = int(channel)

        for l in range(0, 10):
            current_key, current_value = l, self.mixer_led_status[channel * 10 + l]

            if led_level > l:
                if current_value == True:
                    pass
                else:
                    self.set_led(f"{channel}:M{current_key+1}", True)
                    self.mixer_led_status[channel * 10 + current_key] = True
            else:
                if current_value == False:
                    pass
                else:
                    self.set_led(f"{channel}:M{current_key+1}", False)
                    self.mixer_led_status[channel * 10 + current_key] = False

    def mixer_leds_from_fader(self):
        self.mixer_leds_from_value(0, self.fader_values[0])
        self.mixer_leds_from_value(1, self.fader_values[1])

    def startup_animation(self):
        x = 0
        while x < 60:
            toggle = ((x // 20) % 2) == 0

            self.set_led("0:" + str(x % 20), bool(toggle))
            self.set_led("1:" + str(x % 20), bool(toggle))

            time.sleep(0.01)
            x += 1

        self.leds_off()

    def leds_off(self):
        for i in range(0, 20):
            self.set_led("0:" + str(i), False)
            self.set_led("1:" + str(i), False)

    def leds_on(self):
        for i in range(0, 17):
            self.set_led("0:" + str(i), True)
            self.set_led("1:" + str(i), True)
        self.mixer_led_status = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    def shutdown(self):
        self.leds_off()

    def startup(self, animation = True):
        if animation:
            self.startup_animation()
        self.leds_off()