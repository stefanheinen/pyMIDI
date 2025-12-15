I reverse engineered the protocol specification by recording the exchange between the Traktor software and my X1 MK3 and Z1 MK2.

Thanks to @infifox for pointing me in the right direction with his work in his [Mixxx controller scripts for Traktor Z1 MK2 and X1 MK3 controllers](https://github.com/infifox/mixxx-traktor-controllers).

# Displays
A display on the X1 MK3 and the Z1 MK2 has 128 x 64 pixels.
These are divided into eight vertical pages.

These can then be written by concatenating two pages into one long byte sequence and sending the following report (byte sequence, displayed here in hex format):

`e<display_number>00000000<page_number*2>0000200<bytes>`

All the displays are inverted, so invert your image before sending it.

The byte sequence is page-packed MONO_VLSB and can be calculated by the following function:
```Python
from PIL import Image

def image_to_packed_bytes(img: Image.Image):
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

# Example usage:
# img = Image.open("your_image.bmp").convert("1")
# packed_bytes = image_to_packed_bytes(img)
# print(packed_bytes.hex())
```

# LEDs
LEDs can have the following colors:
```Python
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
```

They are written all together by sending the following report:
`80<LED_bytes>`

# Inputs
Inputs are read by reading HID Interrupts with a packet size of 64. The format is:
`01<Input_Controls>`

You can also query the status by requesting input report 1.


# X1 MK3
## LEDs
These are the LED Bytes (in the sequence they have to be sent):

```Python
SHIFT,
Left LOOP,
Right LOOP,
Left PLAY,
Left SYNC,
Right PLAY,
Right SYNC,
Left CUE,
Left REV,
Right CUE,
Right REV,
Left LEFT ARROW,
Left RIGHT ARROW,
Right LEFT ARROW,
Right RIGHT ARROW,
Left H3,
Left H4,
Right H3,
Right H4,
Left H1,
Left H2,
Right H1,
Right H2,
Left FX4_TOGGLE,
Right FX4_TOGGLE,
Left FX3_TOGGLE,
Right FX3_TOGGLE,
Left FX2_TOGGLE,
Right FX2_TOGGLE,
Left FX1_TOGGLE,
Right FX1_TOGGLE,
Left DECKA_L,
Left DECKA_R,
UNKNOWN (Set to 0x7C)
Right DECKA_L,
Right DECKA_R,
Right BACKLIGHT_1,
Right BACKLIGHT_2,
Right BACKLIGHT_3,
Right BACKLIGHT_4,
Right BACKLIGHT_5,
Right BACKLIGHT_6,
UNKNOWN (Set to 0x02)
Left BACKLIGHT_6,
Left BACKLIGHT_5,
Left BACKLIGHT_4,
Left BACKLIGHT_3,
Left BACKLIGHT_2,
Left BACKLIGHT_1,
```

## Inputs
The Inputs have the following sequence. (MSBF)

#### Byte 0:
Bit 0: SHIFT
Bit 1: Left PLAY
Bit 2: Left SYNC
Bit 3: Right PLAY
Bit 4: Right SYNC
Bit 5: Left CUE
Bit 6: Left REV
Bit 7: Right CUE

#### Byte 1:
Bit 0: Right REV
Bit 1: Left LEFT
Bit 2: Left RIGHT
Bit 3: Right LEFT
Bit 4: Right RIGHT
Bit 5: Left H3
Bit 6: Left H4
Bit 7: Right H3

#### Byte 2:
Bit 0: Right H4
Bit 1: Left H1
Bit 2: Left H2
Bit 3: Right H1
Bit 4: Right H2
Bit 5: Left FX4_TOGGLE
Bit 6: Right FX4_TOGGLE
Bit 7: Left FX3_TOGGLE

#### Byte 3:
Bit 0: Right FX3_TOGGLE
Bit 1: Left FX2_TOGGLE
Bit 2: Right FX2_TOGGLE
Bit 3: Left FX1_TOGGLE
Bit 4: Right FX1_TOGGLE
Bit 5: Left DECKA_L
Bit 6: Left DECKA_R
Bit 7: MODE

#### Byte 4:
Bit 0: Right DECKA_L
Bit 1: Right DECKA_R
Bit 2: Left LOOP
Bit 3: Right LOOP
Bit 4: Left BROWSE
Bit 5: Right BROWSE

#### Byte 6:
Bit 0-3: Right Loop Encoder
Bit 4-7: Left Loop Encoder

#### Byte 7:
Bit 0-3: Right Browse Encoder
Bit 4-7: Left Browse Encoder

#### Byte 8:
LSB Left FX4 Knob

#### Byte 9:
MSB Left FX4 Knob

#### Byte 10:
LSB Right FX4 Knob

#### Byte 11:
MSB Right FX4 Knob

#### Byte 12:
LSB Left FX3 Knob

#### Byte 13:
MSB Left FX3 Knob

#### Byte 14:
LSB Right FX3 Knob

#### Byte 15:
MSB Right FX3 Knob

#### Byte 16:
LSB Left FX2 Knob

#### Byte 17:
MSB Left FX2 Knob

#### Byte 18:
LSB Right FX2 Knob

#### Byte 19:
MSB Right FX2 Knob

#### Byte 20:
LSB Left FX1 Knob

#### Byte 21:
MSB Left FX1 Knob

#### Byte 22:
LSB Right FX1 Knob

#### Byte 23:
MSB Right FX1 Knob



# Z1 MK2
## LEDs
These are the LED Bytes (in the sequence they have to be sent):

```Python
Left Mixer1,
Left Mixer2,
Left Mixer3,
Left Mixer4,
Left Mixer5,
Left Mixer6,
Left Mixer7,
Left Mixer8,
Left Mixer9,
Left Mixer10,
Right Mixer1,
Right Mixer2,
Right Mixer3,
Right Mixer4,
Right Mixer5,
Right Mixer6,
Right Mixer7,
Right Mixer8,
Right Mixer9,
Right Mixer10,
Left MODE_MIX,
Left MODE_STEMS,
UNKNOWN (Set to 0x00)
Right MODE_MIX,
Right MODE_STEMS,
Left FX_TOGGLE,
Right FX_TOGGLE,
FX1_BUTTON,
FX2_BUTTON,
FX3_BUTTON,
FX4_BUTTON,
-,
HEADPHONE_L,
HEADPHONE_R,
Left BACKLIGHT_1,
Left BACKLIGHT_2,
Left BACKLIGHT_3,
Left BACKLIGHT_4,
Left BACKLIGHT_5,
Left BACKLIGHT_6,
Right BACKLIGHT_1,
Right BACKLIGHT_2,
Right BACKLIGHT_3,
Right BACKLIGHT_4,
Right BACKLIGHT_5,
Right BACKLIGHT_6,
```

## Inputs
The Inputs have the following sequence. (MSBF)

#### Byte 0:
Bit 0: Left MODE_MIX
Bit 1: Left MODE_STEMS
Bit 2: MODE
Bit 3: Right MODE_MIX
Bit 4: Right MODE_STEMS
Bit 5: Left FX_TOGGLE
Bit 6: Right FX_TOGGLE
Bit 7: FX1_BUTTON

#### Byte 1:
Bit 0: FX2_BUTTON
Bit 1: FX3_BUTTON
Bit 2: FX4_BUTTON
Bit 3: -
Bit 4: HEADPHONE_L
Bit 5: HEADPHONE_R

#### Byte 2:
LSB Left Gain Knob

#### Byte 3:
MSB Left Gain Knob

#### Byte 4:
LSB Left HI Knob

#### Byte 5:
MSB Left HI Knob

#### Byte 6:
LSB Left MID Knob

#### Byte 7:
MSB Left MID Knob

#### Byte 8:
LSB Left LOW Knob

#### Byte 9:
MSB Left LOW Knob

#### Byte 10:
LSB Left FX Knob

#### Byte 11:
MSB Left FX Knob

#### Byte 12:
LSB Right Gain Knob

#### Byte 13:
MSB Right Gain Knob

#### Byte 14:
LSB Right HI Knob

#### Byte 15:
MSB Right HI Knob

#### Byte 16:
LSB Right MID Knob

#### Byte 17:
MSB Right MID Knob

#### Byte 18:
LSB Right LOW Knob

#### Byte 19:
MSB Right LOW Knob

#### Byte 20:
LSB Right FX Knob

#### Byte 21:
MSB Right FX Knob

#### Byte 22:
LSB Headphone Mix Knob

#### Byte 23:
MSB Headphone Mix Knob

#### Byte 24:
LSB Main Volume Knob

#### Byte 25:
MSB Main Volume Knob

#### Byte 26:
LSB Headphone Volume Knob

#### Byte 27:
MSB Headphone Volume Knob

#### Byte 28:
LSB Left Fader

#### Byte 29:
MSB Left Fader

#### Byte 30:
LSB Right Fader

#### Byte 31:
MSB Right Fader

#### Byte 32:
LSB Cross Fader

#### Byte 33:
MSB Cross Fader