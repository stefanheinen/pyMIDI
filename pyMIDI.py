#!/usr/bin/env python3
import os
import threading
from pathlib import Path

import hid
import mido

#### load virtualenv
scriptdir = Path(__file__).resolve().parent
python_home = scriptdir / '.venv'
activate_this = python_home / 'bin' / 'activate_this.py'
if activate_this.exists():
    exec(activate_this.read_text(), {'__file__': str(activate_this)})
else:
    print(f"Virtual environment not found at \"{activate_this}\"")
    exit(os.EX_SOFTWARE)
#### end load virtualenv


import pyautogui
import time
import logging
from logging import info, warning, error
from queue import Queue

from devices.hid.traktor_x1_mk3 import HIDDevice as X1_HID
from devices.hid.traktor_z1_mk2 import HIDDevice as Z1_HID
from devices.midi.traktor_x1_mk3 import Device as X1_MIDI
from devices.midi.traktor_z1_mk2 import Device as Z1_MIDI

from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device

from event_to_app_maps import traktor_x1_davinci_resolve,traktor_z1_davinci_resolve

logging.basicConfig(level=logging.INFO, format="%(message)s")

if __name__ == '__main__':
    pyautogui.PAUSE = 0.005

    devices = [
                X1_HID(),
                X1_MIDI(),
                Z1_HID(),
                Z1_MIDI()
               ]
    device_to_app_maps = {
                            devices[0]: traktor_x1_davinci_resolve.EventToAppToAppMap(devices[0]),
                            devices[1]: traktor_x1_davinci_resolve.EventToAppToAppMap(devices[1]),
                            devices[2]: traktor_z1_davinci_resolve.EventToAppToAppMap(devices[2]),
                            devices[3]: traktor_z1_davinci_resolve.EventToAppToAppMap(devices[3])
    }


    # start thread that looks for known devices, starts them, and connects them to the in queue
    in_queue = Queue()
    stop_device_control_thread = threading.Event()

    def device_control_function(in_queue: Queue):
        def startup(d, animation: bool = True, wait: bool = True):
            if wait:
                time.sleep(3)
            d.startup(animation)

            if d in device_to_app_maps:
                device_to_app_maps[d].init()
            d.set_status("ready")

        try:
            while not stop_device_control_thread.is_set():
                connected_hid_devices = hid.enumerate()
                for cd in connected_hid_devices:
                    # check if it's a known device
                    for d in devices:
                        if not d.PROTOCOL == "HID": continue
                        if d.VENDOR_ID == cd["vendor_id"] and d.PRODUCT_ID == cd["product_id"]:
                            device_status = d.get_status()
                            if device_status == "" or device_status == "disconnected":
                                animation = (device_status == "")
                                try:
                                    d.open(in_queue)
                                    logging.info(f"Opened device \"{d.PROTOCOL}:{d.DEVICE_NAME}\"")
                                    threading.Thread(target=startup, args=(d,animation, not animation), daemon=True).start()
                                except Exception as e:
                                    warning(f"Could not open device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

                try:
                    connected_midi_devices = mido.get_input_names()
                except:
                    connected_midi_devices = []
                for cd in connected_midi_devices:
                    # check if it's a known device
                    for d in devices:
                        if not d.PROTOCOL == "MIDI": continue
                        if d.MIDI_port_name == cd:
                            device_status = d.get_status()
                            if device_status == "" or device_status == "disconnected":
                                animation = (device_status == "")
                                try:
                                    d.open(in_queue)
                                    logging.info(f"Opened device \"{d.PROTOCOL}:{d.DEVICE_NAME}\"")
                                    threading.Thread(target=startup, args=(d,animation, not animation), daemon=True).start()
                                except Exception as e:
                                    warning(f"Could not open device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

                for d in devices:
                    if d.get_status() == "": d.set_status("disconnected")
                time.sleep(0.5)
        finally:
            for d in devices:
                try:
                    d.shutdown()
                except Exception as e:
                    error(f"Error shutting down device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

            time.sleep(0.2) # give devices some time for shutdown procedure before shutting down sender and receiver threads

            for d in devices:
                try:
                    d.close()
                except Exception as e:
                    error(f"Error closing device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")
            logging.info("Device manager thread shutting down.")

    device_control_thread = threading.Thread(target=device_control_function, args=(in_queue,))
    device_control_thread.start()

    print()
    print("Listening... Press Ctrl+C to stop.")
    # main loop # interrupt on keyboard exit
    try:
        while True:
            # check if there are new events and process them
            while not in_queue.empty():
                device, event = in_queue.get()

                if event:
                    info(device.PROTOCOL + ":" + device.DEVICE_NAME + ":" + event)

                    # standard button reactions (make LED red if button pushed)
                    channel, control, value = event.split(":")
                    if value == "D":
                        if device.PROTOCOL == "MIDI":
                            device.set_led(f"{channel}:{control}", True)
                        if isinstance(device, Native_Instruments_HID_Device):
                            device.set_led(f"{channel}:{control}", device.LEDColor.RED)
                    if value == "U":
                        if device.PROTOCOL == "MIDI":
                            device.set_led(f"{channel}:{control}", False)
                        if isinstance(device, Native_Instruments_HID_Device):
                            device.set_led(f"{channel}:{control}", device.LEDColor.WHITE)
                    device.flush_leds()

                if device in device_to_app_maps:
                    device_to_app_maps[device].handle_event(event)
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("Exiting...")
        stop_device_control_thread.set()
        device_control_thread.join()

        for d in devices:
            d.send_thread.join()
            d.receive_thread.join()
