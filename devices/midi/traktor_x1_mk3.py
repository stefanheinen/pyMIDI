import time

import mido

from .midi_device import MIDIEvent, MIDI_Device

class Device(MIDI_Device):
    MIDI_port_name = "TRAKTOR X1 MK3"
    DEVICE_NAME = "TRAKTOR X1 MK3"
    DISPLAY_SIZE = (128, 64)
    DISPLAY_COUNT = 5

    def __init__(self):
        super().__init__()
        pass

    def decode_events(self, msg):
        ### Browse Encoder ###
        if MIDIEvent(control=20, value=63) == msg: return [f"{msg.channel}:BROWSE:L"] # left
        if MIDIEvent(control=20, value=65) == msg: return [f"{msg.channel}:BROWSE:R"] # right
        if MIDIEvent(note=20, velocity=127) == msg: return [f"{msg.channel}:BROWSE:D"] # down
        if MIDIEvent(note=20, velocity=0) == msg: return [f"{msg.channel}:BROWSE:U"] # down

        ### Loop Encoder ###
        if MIDIEvent(control=21, value=63) == msg: return [f"{msg.channel}:LOOP:L"] # left
        if MIDIEvent(control=21, value=65) == msg: return [f"{msg.channel}:LOOP:R"] # right
        if MIDIEvent(note=21, velocity=127) == msg: return [f"{msg.channel}:LOOP:D"] # down
        if MIDIEvent(note=21, velocity=0) == msg: return [f"{msg.channel}:LOOP:U"] # down

        ### Play Button ###
        if MIDIEvent(note=10, velocity=127) == msg: return [f"{msg.channel}:PLAY:D"] # down
        if MIDIEvent(note=10, velocity=0) == msg: return [f"{msg.channel}:PLAY:U"] # up

        ### Sync Button ###
        if MIDIEvent(note=11, velocity=127) == msg: return [f"{msg.channel}:SYNC:D"] # down
        if MIDIEvent(note=11, velocity=0) == msg: return [f"{msg.channel}:SYNC:U"] # up

        ### 1 ###
        if MIDIEvent(note=2, velocity=127) == msg: return [f"{msg.channel}:H1:D"] # down
        if MIDIEvent(note=2, velocity=0) == msg: return [f"{msg.channel}:H1:U"] # up

        ### 2 ###
        if MIDIEvent(note=3, velocity=127) == msg: return [f"{msg.channel}:H2:D"] # down
        if MIDIEvent(note=3, velocity=0) == msg: return [f"{msg.channel}:H2:U"] # up

        ### 3 ###
        if MIDIEvent(note=4, velocity=127) == msg: return [f"{msg.channel}:H3:D"] # down
        if MIDIEvent(note=4, velocity=0) == msg: return [f"{msg.channel}:H3:U"] # up

        ### 4 ###
        if MIDIEvent(note=5, velocity=127) == msg: return [f"{msg.channel}:H4:D"] # down
        if MIDIEvent(note=5, velocity=0) == msg: return [f"{msg.channel}:H4:U"] # up

        ### Left Arrow ###
        if MIDIEvent(note=6, velocity=127) == msg: return [f"{msg.channel}:LEFT:D"] # down
        if MIDIEvent(note=6, velocity=0) == msg: return [f"{msg.channel}:LEFT:U"] # up

        ### Right Arrow ###
        if MIDIEvent(note=7, velocity=127) == msg: return [f"{msg.channel}:RIGHT:D"] # down
        if MIDIEvent(note=7, velocity=0) == msg: return [f"{msg.channel}:RIGHT:U"] # up

        ### Cue ###
        if MIDIEvent(note=8, velocity=127) == msg: return [f"{msg.channel}:CUE:D"] # down
        if MIDIEvent(note=8, velocity=0) == msg: return [f"{msg.channel}:CUE:U"] # up

        ### Reverse ###
        if MIDIEvent(note=9, velocity=127) == msg: return [f"{msg.channel}:REV:D"] # down
        if MIDIEvent(note=9, velocity=0) == msg: return [f"{msg.channel}:REV:U"] # up

        ### FX1 ###
        if MIDIEvent(note=16, velocity=127) == msg: return [f"{msg.channel}:FX1_TOGGLE:D"] # down
        if MIDIEvent(note=16, velocity=0) == msg: return [f"{msg.channel}:FX1_TOGGLE:U"] # up

        ### FX2 ###
        if MIDIEvent(note=17, velocity=127) == msg: return [f"{msg.channel}:FX2_TOGGLE:D"] # down
        if MIDIEvent(note=17, velocity=0) == msg: return [f"{msg.channel}:FX2_TOGGLE:U"] # up

        ### FX3 ###
        if MIDIEvent(note=18, velocity=127) == msg: return [f"{msg.channel}:FX3_TOGGLE:D"] # down
        if MIDIEvent(note=18, velocity=0) == msg: return [f"{msg.channel}:FX3_TOGGLE:U"] # up

        ### FX4 ###
        if MIDIEvent(note=19, velocity=127) == msg: return [f"{msg.channel}:FX4_TOGGLE:D"] # down
        if MIDIEvent(note=19, velocity=0) == msg: return [f"{msg.channel}:FX4_TOGGLE:U"] # up

        ### Deck Assign L ###
        if MIDIEvent(note=0, velocity=127) == msg: return [f"{msg.channel}:DECKA_L:D"] # down
        if MIDIEvent(note=0, velocity=0) == msg: return [f"{msg.channel}:DECKA_L:U"] # up

        ### Deck Assign R ###
        if MIDIEvent(note=1, velocity=127) == msg: return [f"{msg.channel}:DECKA_R:D"] # down
        if MIDIEvent(note=1, velocity=0) == msg: return [f"{msg.channel}:DECKA_R:U"] # up

        ### FX Knob 1 ###
        if MIDIEvent(control=16) == msg: return [f"{msg.channel}:FX1:{msg.value}"]

        ### FX Knob 2 ###
        if MIDIEvent(control=17) == msg: return [f"{msg.channel}:FX2:{msg.value}"]

        ### FX Knob 3 ###
        if MIDIEvent(control=18) == msg: return [f"{msg.channel}:FX3:{msg.value}"]

        ### FX Knob 4 ###
        if MIDIEvent(control=19) == msg: return [f"{msg.channel}:FX4:{msg.value}"]

        return None

    def set_led(self, led, color):
        channel, led = led.split(":", 1)

        channel = int(channel)

        if color:
            velocity = 127
        else:
            velocity = 0

        if led == "DECKA_L" or led == "0": self.send_queue.put(mido.Message('note_on', channel=channel, note=0, velocity=velocity))
        if led == "DECKA_R" or led == "1": self.send_queue.put(mido.Message('note_on', channel=channel, note=1, velocity=velocity))

        if led == "FX1_TOGGLE" or led == "2": self.send_queue.put(mido.Message('note_on', channel=channel, note=16, velocity=velocity))
        if led == "FX2_TOGGLE" or led == "3": self.send_queue.put(mido.Message('note_on', channel=channel, note=17, velocity=velocity))
        if led == "FX3_TOGGLE" or led == "4": self.send_queue.put(mido.Message('note_on', channel=channel, note=18, velocity=velocity))
        if led == "FX4_TOGGLE" or led == "5": self.send_queue.put(mido.Message('note_on', channel=channel, note=19, velocity=velocity))

        if led == "LOOP" or led == "6": self.send_queue.put(mido.Message('note_on', channel=channel, note=21, velocity=velocity))

        if led == "H1" or led == "7": self.send_queue.put(mido.Message('note_on', channel=channel, note=2, velocity=velocity))
        if led == "H2" or led == "8": self.send_queue.put(mido.Message('note_on', channel=channel, note=3, velocity=velocity))
        if led == "H3" or led == "9": self.send_queue.put(mido.Message('note_on', channel=channel, note=4, velocity=velocity))
        if led == "H4" or led == "10": self.send_queue.put(mido.Message('note_on', channel=channel, note=5, velocity=velocity))

        if led == "LEFT" or led == "11": self.send_queue.put(mido.Message('note_on', channel=channel, note=6, velocity=velocity))
        if led == "RIGHT" or led == "12": self.send_queue.put(mido.Message('note_on', channel=channel, note=7, velocity=velocity))

        if led == "CUE" or led == "13": self.send_queue.put(mido.Message('note_on', channel=channel, note=8, velocity=velocity))
        if led == "REV" or led == "14": self.send_queue.put(mido.Message('note_on', channel=channel, note=9, velocity=velocity))

        if led == "PLAY" or led == "15": self.send_queue.put(mido.Message('note_on', channel=channel, note=10, velocity=velocity))
        if led == "SYNC" or led == "16": self.send_queue.put(mido.Message('note_on', channel=channel, note=11, velocity=velocity))

    def startup_animation(self):
        x = 0
        while x < 53:
            toggle = ((x // 18) % 2) == 0
            self.set_led("0:" + str(x % 18), bool(toggle))
            self.set_led("1:" + str(x % 18), bool(toggle))

            time.sleep(0.01)
            x += 1

        self.leds_off()

    def leds_off(self):
        for i in range(0, 17):
            self.set_led("0:" + str(i), False)
            self.set_led("1:" + str(i), False)

    def leds_on(self):
        for i in range(0, 17):
            self.set_led("0:" + str(i), True)
            self.set_led("1:" + str(i), True)

    def shutdown(self):
        self.leds_off()

    def startup(self, animation = True):
        if animation:
            self.startup_animation()
        self.leds_off()