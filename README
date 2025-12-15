# pyMIDI

Control your computer with a MIDI or HID Device.

I was looking for a way to control Davinci Resolve with my Native Instruments controllers,
and so I wrote this little command line tool that listens to MIDI or HID messages and executes pyautogui commands.

Devices are defined in `devices/midi` and `devices/hid` respectively.

These devices generate events that can be consumed by `event_to_app_maps`.

Everything is still a bit brittle, and not everything is programmed thread safe.

## Requirements
- python3.13 (very probably also works with earlier versions)
- hid and hidapi installed on the system
- mido
- pillow
- pyautogui
- python-rtmidi

## Native Instruments USB HID Specification
If you're interested in how the controller talks to your computer,
here's what I found out reverse engineering the Traktor X1 MK3's and Z1 MK2's protocol:

[Protocol Specification](docs/Native Instruments Traktor X1 MK3 and Z1 MK2 HID Protocol Specification.md)