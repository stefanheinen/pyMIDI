# pyConduktor

Control your computer with a HID or MIDI Device.

I was looking for a way to control Davinci Resolve with my Native Instruments controllers,
and so I wrote this little command line tool that listens to MIDI or HID messages and executes pyautogui commands.

Devices are defined in `devices/midi` and `devices/hid` respectively.
They have to be imported in `devices/__init__.py` to be recognized.

These devices generate events that can be consumed by `event_to_app_maps`.

Everything is still a bit brittle and for now only works on macOS if you don't comment out the launchd and statusbar specific code.

## Requirements
- python3.13 (very probably also works with earlier versions)
- macos with pyobjc and launchd-plist for statusbar integration and autostart
- hid and hidapi installed on the system
- mido
- pillow
- pyautogui
- pyyaml
- platformdirs
- requests

## Native Instruments USB HID Specification
If you're interested in how the controller talks to your computer,
here's what I found out reverse engineering the Traktor X1 MK3's and Z1 MK2's protocol:

[Protocol Specification](docs/Native%20Instruments%20Traktor%20X1%20MK3%20and%20Z1%20MK2%20HID%20Protocol%20Specification.md)