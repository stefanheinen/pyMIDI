#!/usr/bin/env python3
import abc
import argparse
import inspect
from typing import get_type_hints, get_origin, Union
import pathlib
import queue
from typing import List, Tuple
from typing import get_type_hints, get_args

import time
import threading
import logging
import uuid
from logging import info, warning, error, debug
from queue import Queue

import hid
import mido
import pyautogui
from PyObjCTools import AppHelper
from AppKit import NSApp
import platformdirs
import yaml

import launchAgent
import status_icon

import devices.device

import event_to_app_maps

CONFIG_DIR = platformdirs.user_config_dir("pyMIDI", ensure_exists=True)

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

devices_lock = threading.RLock()
device_event_queue: queue.Queue = queue.Queue()

main_loop_thread: threading.Thread | None = None
device_control_thread: threading.Thread | None = None
gui_loop_thread: threading.Thread | None = None

main_loop_stop = threading.Event()
device_control_loop_stop = threading.Event()
gui_loop_stop = threading.Event()


class DeviceManager:
    def __init__(self, device_event_queue, device_classes, event_map_classes):
        self._device_classes = device_classes
        self._event_map_classes = event_map_classes

        self._devices_lock = threading.RLock()

        self._device_control_loop_thread = threading.Thread()
        self._device_control_loop_stop = threading.Event()

        self._device_event_queue = device_event_queue

        self._initDevicesFromDeviceClasses(self._device_classes)


    def _initDevicesFromDeviceClasses(self, device_classes: List[devices.device]):
        def init_param_accepts(cls, param_name: str, candidate_type: type) -> bool:
            """
            Returns True if candidate_type can be passed to cls.__init__ for parameter param_name.
            Works with Union types and accounts for subclass relationships.
            """
            hints = get_type_hints(cls.__init__)
            if param_name not in hints:
                return False

            hint = hints[param_name]
            origin = get_origin(hint)

            # Single type (not a union)
            if origin is None:
                return issubclass(candidate_type, hint)

            # Union type
            if origin is Union:
                return any(issubclass(candidate_type, t) for t in get_args(hint))

            # Other types (rare)
            return issubclass(candidate_type, hint)

        self._devices = {}
        with self._devices_lock:
            for d in device_classes:
                instance = d()

                # find all compatible event_maps
                event_maps = []

                for em in self._event_map_classes:
                    if init_param_accepts(em, "device", d):
                        event_maps.append(em(instance))

                self._devices[instance] = {
                                            "status": None,
                                            "eventToAppMaps": event_maps,
                                            "activeMap": None
                                          }


    def getDeviceById(self, id: uuid.UUID) -> devices.device.Device | None:
        with self._devices_lock:
            for d in self._devices:
                if d.id == id:
                    return d
            return None

    def getActiveMapByDeviceId(self, device_id: uuid.UUID) -> event_to_app_maps.event_to_app_map.EventToAppMap | None:
        with self._devices_lock:
            for d, properties in self._devices.items():
                if d.id == device_id:
                    if "activeMap" in properties:
                        return properties["activeMap"]
            return None

    def setActiveMapForDeviceId(self, device_id: uuid.UUID, eventmap_name: str):
        with self._devices_lock:
            d, p = None, None
            for device, properties in self._devices.items():
                if device.id == device_id:
                    p = properties
                    d = device
                    break

            for i, eventmap in enumerate(p["eventToAppMaps"]):
                if eventmap.NAME == eventmap_name:
                    if "activeMap" in p and not p["activeMap"] is None:
                        p["activeMap"].shutdown(True)
                    self._devices[d]["activeMap"] = self._devices[d]["eventToAppMaps"][i]
                    eventmap.init()
                    info(f"Activated eventMap: {eventmap_name} for device: {d.PROTOCOL}:{d.DEVICE_NAME}")

    def setActiveMapForDeviceName(self, device_protocol:str, device_name: str, eventmap_name: str):
        device = None
        with self._devices_lock:
            for d in self._devices:
                if d.PROTOCOL == device_protocol and d.DEVICE_NAME == device_name:
                    device = d
                    break

        if device:
            self.setActiveMapForDeviceId(device.id, eventmap_name)
            return True
        else:
            return False


    def getDeviceStates(self) -> List[Tuple[uuid.UUID, str, str, str]]:
        status_list = []

        with self._devices_lock:
            for d, properties in self._devices.items():
                event_maps = []
                for em in properties["eventToAppMaps"]:
                    active = (em == properties["activeMap"])
                    event_maps.append((em.NAME, active))

                status_list.append((d.id, d.PROTOCOL, d.DEVICE_NAME, d.get_status(), event_maps))

        return status_list

    def _device_control_loop(self):
        # thread that looks for known devices, starts them, and connects them to the device_event_queue
        def startup_device(d, device_to_app_map, animation: bool = True, wait: bool = True):
            if wait:
                time.sleep(3)

            d.init(animation)

            if device_to_app_map:
                device_to_app_map.init()
            d.set_status("ready")

        try:
            while not self._device_control_loop_stop.is_set():
                connected_hid_devices = [("HID", d) for d in hid.enumerate()]
                try:
                    connected_midi_devices = [("MIDI", d) for d in mido.get_input_names()]
                except:
                    connected_midi_devices = []

                for cd in connected_hid_devices + connected_midi_devices:
                    # check if it's a known device
                    with self._devices_lock:
                        for d, properties in self._devices.items():
                            if (d.PROTOCOL == "HID" == cd[0] and
                                    d.VENDOR_ID == cd[1]["vendor_id"] and d.PRODUCT_ID == cd[1]["product_id"]
                                    or d.PROTOCOL == "MIDI" == cd[0] and
                                    d.MIDI_port_name == cd[1]):
                                device_status = d.get_status()
                                if device_status == "" or device_status == "disconnected":
                                    animation = (device_status == "")
                                    try:
                                        d.open(self._device_event_queue)
                                        logging.info(f"Opened device \"{d.PROTOCOL}:{d.DEVICE_NAME}\"")
                                        threading.Thread(target=startup_device,
                                                         args=(d, properties["activeMap"], animation, not animation),
                                                         daemon=True).start()
                                    except Exception as e:
                                        warning(f"Could not open device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

                with self._devices_lock:
                    for d in self._devices:
                        if d.get_status() == "": d.set_status("disconnected")
                time.sleep(0.5)
        finally:
            for d in self._devices:
                try:
                    d.shutdown()
                except Exception as e:
                    error(f"Error shutting down device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

            time.sleep(0.3)  # give devices some time for shutdown procedure before shutting down sender and receiver threads

            for d in self._devices:
                try:
                    d.close()
                except Exception as e:
                    error(f"Error closing device \"{d.PROTOCOL}:{d.DEVICE_NAME}\": {str(e)}")

    def start(self):
        self._device_control_loop_stop.clear()
        self._device_control_loop_thread = threading.Thread(target=self._device_control_loop, args=())
        self._device_control_loop_thread.start()
        pass

    def stop(self, wait: bool = False):
        active_maps = []
        with self._devices_lock:
            for d, properties in self._devices.items():
                if properties["activeMap"]:
                    active_maps.append(properties["activeMap"])

        for em in active_maps:
            em.shutdown()

        for em in active_maps:
            em.shutdown_join()

        self._device_control_loop_stop.set()
        if wait:
            self._device_control_loop_thread.join()

    def stop_join(self):
        self._device_control_loop_thread.join()


def main_loop(dm: DeviceManager, device_event_queue: Queue):
    # main loop that reads events from the device_event_queue
    # and passes them to the event to app maps

    while not main_loop_stop.is_set():
        while not device_event_queue.empty():
            device_id, protocol, device_name, event = device_event_queue.get()

            if event:
                info(protocol + ":" + device_name + ":" + event)

                event_map = dm.getActiveMapByDeviceId(device_id)
                if event_map:
                    event_map.handle_event(event)
            device_event_queue.task_done()
        time.sleep(0.05)


def gui_loop(STATUSICON_APP, dm: DeviceManager, status_icon_queue, gui_loop_stop):
    # check for status bar icon interaction, or updates necessary
    device_menu_update_necessary = False

    devices_last_state = dm.getDeviceStates()

    while not gui_loop_stop.is_set():
        current_state = dm.getDeviceStates()
        if not devices_last_state == current_state:
            device_menu_update_necessary = True

        try:
            event = status_icon_queue.get(timeout=0.3)
        except queue.Empty:
            event = None

        if event:
            if event.event == "EXIT":
                quit(dm, STATUSICON_APP)
                break

            if event.event == "DEVICEMAPSELECT":
                # make new map the active map
                device_id, eventmap_name = event.parameters
                dm.setActiveMapForDeviceId(device_id, eventmap_name)
                device_menu_update_necessary = True

        if device_menu_update_necessary:
            STATUSICON_APP.updateDeviceMenu(current_state)


def quit(dm: DeviceManager, STATUSICON_APP = None):
    logging.info("Shutting down...")

    main_loop_stop.set()
    if gui_loop_thread:
        if not threading.current_thread() == gui_loop_thread:
            gui_loop_stop.set()

    dm.stop()

    config = {"devices": {}}
    for id, protocol, name, _, _ in dm.getDeviceStates():
        active_map = dm.getActiveMapByDeviceId(id)
        if active_map:
            config["devices"][f"{protocol}:{name}"] = {"activeMap": active_map.NAME}
        else:
            config["devices"][f"{protocol}:{name}"] = {"activeMap": ""}
    store_config(config)

    main_loop_thread.join()
    if gui_loop_thread and not threading.current_thread() == gui_loop_thread:
        gui_loop_thread.join()
    dm.stop_join()

    if STATUSICON_APP:
        NSApp.terminate_(STATUSICON_APP)

def load_config():
    config_file_path = pathlib.Path(CONFIG_DIR) / "config.yaml"
    with open(config_file_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

def store_config(config: dict):
    config_file_path = pathlib.Path(CONFIG_DIR) / "config.yaml"
    with open(config_file_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)


if __name__ == '__main__':
    debug(CONFIG_DIR)
    parser = argparse.ArgumentParser(
        description="pyMIDI lets you connect HID/MIDI controllers and execute actions on control changes"
    )

    parser.add_argument(
        "--statusbar",
        action="store_true",
        help="Display icon in statusbar."
    )

    parser.add_argument(
        "--autostart",
        type=str,
        default=None,
        help="Activate/deactivate autostart on login."
    )

    args = parser.parse_args()

    if args.autostart in ("true", "1", "yes", "on"):
        launchAgent.activate()
        exit()
    if args.autostart in ("false", "0", "no", "off"):
        launchAgent.deactivate()
        launchAgent.remove()
        exit()
    if args.autostart in ("?", "get"):
        info(f"Autostart: {launchAgent.get_activated_status()}")
        exit()

    pyautogui.PAUSE = 0.05

    # loop through all classes of module event_to_app_maps
    # if they're not an abstract class and they have the NAME attribute set (they are a
    # concrete implementation of an event_map), add them to the list of available classes
    available_event_map_classes = []
    def concrete_subclasses(base):
        for cls in base.__subclasses__():
            yield from concrete_subclasses(cls)
            if not inspect.isabstract(cls):
                yield cls

    for cls in concrete_subclasses(event_to_app_maps.event_to_app_map.EventToAppMap):
        if hasattr(cls, "NAME"):
            available_event_map_classes.append(cls)

    # loop through all classes of module devices and get all available devices
    available_device_classes = []
    for cls in concrete_subclasses(devices.device.Device):
        if hasattr(cls, "DEVICE_NAME"):
            available_device_classes.append(cls)

    debug(available_device_classes)

    deviceManager = DeviceManager(device_event_queue, available_device_classes, available_event_map_classes)

    debug(config:= load_config())

    for device_port_name, device_config in config["devices"].items():
        device_port_name_split = device_port_name.split(":")
        deviceManager.setActiveMapForDeviceName(device_port_name_split[0], device_port_name_split[1], device_config["activeMap"])

    deviceManager.start()


    main_loop_thread = threading.Thread(target=main_loop, args=(deviceManager, device_event_queue))
    main_loop_thread.start()

    if args.statusbar:
        # create the icon
        status_icon_queue = queue.Queue()
        STATUSICON_APP = status_icon.App(status_icon_queue)
        STATUSICON_APP.updateDeviceMenu(deviceManager.getDeviceStates())
        gui_loop_thread = threading.Thread(target=gui_loop, args=(STATUSICON_APP, deviceManager, status_icon_queue, gui_loop_stop))
        gui_loop_thread.start()

        # run the app main loop
        AppHelper.runEventLoop()
    else:
        print()
        print("Listening... Press Ctrl+C to stop.")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            quit(deviceManager)
