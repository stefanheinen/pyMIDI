import os
import subprocess
import threading
import time
from logging import error, debug
from functools import wraps

import requests
from requests.auth import HTTPBasicAuth

from devices.hid.native_instruments_hid_device import Native_Instruments_HID_Device
from devices.hid.traktor_z1_mk2 import HIDDevice as Z1_HID_Device
from devices.midi.traktor_z1_mk2 import Device as Z1_MIDI_Device

from event_to_app_maps.native_instruments_event_to_app_map import NIEventToAppMap


class EventToAppToAppMap(NIEventToAppMap):
    NAME = "Spotify + VLC"
    APP_NAME_DISPLAY = 1
    APPLICATION_NAME = "Spotify\nVLC"
    HELP_BUTTON = "2:MODE"
    HELP_DISPLAYS = (1, 1)

    MOD = {}    # saves status about currently set modifiers (to enable key combinations like SHIFT + PLAY)

    def __init__(self, device: Z1_HID_Device | Z1_MIDI_Device):
        super().__init__(device)
        self.device = device

        self.vlc = VLCController(password="blubber132")
        self.spotify = SpotifyController()
        self.system = SystemController()

    def init(self):
        super().init()

        if self.vlc.get_playing_state() == "playing":
            self.state["vlc_playing"] = True
            self.BUTTON_COLORS["1:FX_TOGGLE"] = (self.c.GREEN, self.c.RED)
        else:
            self.state["vlc_playing"] = False

        if self.spotify.get_playing_state() == "playing":
            self.state["spotify_playing"] = True
            self.BUTTON_COLORS["0:FX_TOGGLE"] = (self.c.GREEN, self.c.RED)
        else:
            self.state["spotify_playing"] = False

        self.state["scrolling_text_vlc_stop_event"] = threading.Event()
        self.launch_interface_thread("scrolling_text_vlc", self.scrolling_text_thread_function,
                                     (2, self.vlc.get_currently_playing_title, self.vlc.get_currently_playing_artist))

        self.state["scrolling_text_spotify_stop_event"] = threading.Event()
        self.launch_interface_thread("scrolling_text_spotify", self.scrolling_text_thread_function,
                                     (0, self.spotify.get_currently_playing_title, self.spotify.get_currently_playing_artist))

    def __del__(self):
        self.stop_interface_thread("scrolling_text_vlc")

    HELP_TEXTS = {
        # "0:MODE_MIX": ("Left Mix", "(unassigned)"),
        # "0:MODE_STEMS": ("Left Stems", "(unassigned)"),
        # "1:MODE_MIX": ("Right Mix", "(unassigned)"),
        # "1:MODE_STEMS": ("Right Stems", "(unassigned)"),
        "0:FX_TOGGLE": ("Spotify", "Play/Pause"),
        "1:FX_TOGGLE": ("VLC", "Play/Pause"),
        "2:FX1_BUTTON": ("Spotify", "Previous"),
        "2:FX2_BUTTON": ("VLC", "Previous"),
        "2:FX3_BUTTON": ("Spotify", "Next"),
        "2:FX4_BUTTON": ("VLC", "Next"),
        "0:FADER": ("Spotify", "Volume"),
        "1:FADER": ("VLC", "Volume"),
        "2:MAIN": ("System", "Volume"),
        # "2:HEADPHONE_L": ("Left Headp", "(unassigned)"),
        # "2:HEADPHONE_R": ("Right Headp", "(unassigned)"),
    }

    c = Native_Instruments_HID_Device.LEDColor
    BUTTON_COLORS = {
        "0:MODE_MIX": (c.BLACK, c.RED),
        "0:MODE_STEMS": (c.BLACK, c.RED),
        "1:MODE_MIX": (c.BLACK, c.RED),
        "1:MODE_STEMS": (c.BLACK, c.RED),
        "0:FX_TOGGLE": (c.GREEN_DIM, c.RED),
        "1:FX_TOGGLE": (c.GREEN_DIM, c.RED),
        "2:FX1_BUTTON": (c.YELLOW, c.RED),
        "2:FX2_BUTTON": (c.YELLOW, c.RED),
        "2:FX3_BUTTON": (c.YELLOW, c.RED),
        "2:FX4_BUTTON": (c.YELLOW, c.RED),
        "2:-": (c.BLACK, c.RED),
        "2:HEADPHONE_L": (c.BLACK, c.RED),
        "2:HEADPHONE_R": (c.BLACK, c.RED),
    }

    def init_leds(self):
        self.device.mixer_leds_from_fader()
        super().init_leds()

    def set_default_led_color(self, led, color_index = 0):
        channel, led_name = led.split(":")
        if led_name in [f"M{i}" for i in range(1, 11)]:
            return

        super().set_default_led_color(led, color_index)

    def handle_event(self, event: str):
        super().handle_event(event)

        channel, control, value = event.split(":")
        if control == "FADER":
            self.device.mixer_leds_from_fader()

        if self.MOD["HELP"]: return

        if event == "0:FX_TOGGLE:U":
            if self.state["spotify_playing"]:
                self.BUTTON_COLORS["0:FX_TOGGLE"] = (self.c.GREEN_DIM, self.c.RED)
                self.spotify.pause()
                self.state["spotify_playing"] = False
            else:
                self.BUTTON_COLORS["0:FX_TOGGLE"] = (self.c.GREEN, self.c.RED)
                self.spotify.play()
                self.state["spotify_playing"] = True

        if event == "1:FX_TOGGLE:U":
            if self.state["vlc_playing"]:
                self.BUTTON_COLORS["1:FX_TOGGLE"] = (self.c.GREEN_DIM, self.c.RED)
                self.vlc.pause()
                self.state["vlc_playing"] = False
            else:
                self.BUTTON_COLORS["1:FX_TOGGLE"] = (self.c.GREEN, self.c.RED)
                self.vlc.play()
                self.state["vlc_playing"] = True

        if event == "2:FX1_BUTTON:U":
            self.spotify.previous()

        if event == "2:FX3_BUTTON:U":
            self.spotify.next()

        if event == "2:FX2_BUTTON:U":
            self.vlc.previous()

        if event == "2:FX4_BUTTON:U":
            self.vlc.next()

        if channel == "0" and control == "FX":
                new_position = float(value) / 4095
                self.spotify.seek(new_position)
        if channel == "1" and control == "FX":
                new_position = float(value) / 4095
                self.vlc.seek(new_position)

        if channel == "2" and control == "MAIN":
            self.system.set_volume(int(100/4095 * int(value)))

        if channel == "0" and control == "FADER":
            volume = int(100/4095 * int(value))
            self.spotify.set_volume(volume)

        if channel == "1" and control == "FADER":
            volume = int(256/4095 * int(value))
            self.vlc.set_volume(volume)

        self.set_default_led_colors(event)
        self.device.flush_leds()

    def scrolling_text_thread_function(self, stop_event: threading.Event, display: int, text_function_line1: callable = lambda: "", text_function_line2: callable = lambda: ""):
        while not stop_event.is_set():
            line1 = f"{text_function_line1()}"
            line2 = f"{text_function_line2()}"
            self.device.write_text_to_display(display, f"{line1}\n{line2}")
            time.sleep(0.4)


def latest_value(func):
    """
    Decorator for instance methods: only processes the latest value.
    Fixed delay of 2 seconds after the last update before the worker thread exits.
    Uses an Event for efficient waking.
    """
    attr_lock = f"_{func.__name__}_lock"
    attr_value = f"_{func.__name__}_latest"
    attr_thread = f"_{func.__name__}_thread"
    attr_event = f"_{func.__name__}_event"

    @wraps(func)
    def wrapper(self, value):
        # Initialize per-instance attributes if missing
        if not hasattr(self, attr_lock):
            setattr(self, attr_lock, threading.Lock())
        if not hasattr(self, attr_value):
            setattr(self, attr_value, None)
        if not hasattr(self, attr_event):
            setattr(self, attr_event, threading.Event())

        lock = getattr(self, attr_lock)
        event = getattr(self, attr_event)

        # Store latest value and wake worker
        with lock:
            setattr(self, attr_value, value)
            event.set()

        # Start worker thread if not running
        thread = getattr(self, attr_thread, None)
        if thread is None or not thread.is_alive():
            def worker():
                last_event_time = time.time()
                while True:
                    remaining = 2.0 - (time.time() - last_event_time)
                    if remaining <= 0:
                        break
                    # Wait until a new value arrives or timeout
                    event_is_set = event.wait(timeout=remaining)

                    with lock:
                        val = getattr(self, attr_value)
                        setattr(self, attr_value, None)
                        event.clear()

                    if val is not None:
                        func(self, val)
                        last_event_time = time.time()

            thread = threading.Thread(target=worker, daemon=True)
            setattr(self, attr_thread, thread)
            thread.start()

    return wrapper

def timed_cache(ttl: float):
    """
    Returns a cached value if function is called again within ttl
    """
    def decorator(func):
        attr_cache = f"_{func.__name__}_cache"
        attr_lock = f"_{func.__name__}_lock"

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Initialize per-instance lock and cache
            if not hasattr(self, attr_cache):
                setattr(self, attr_cache, {"value": None, "timestamp": 0})
            if not hasattr(self, attr_lock):
                setattr(self, attr_lock, threading.Lock())

            cache = getattr(self, attr_cache)
            lock = getattr(self, attr_lock)
            now = time.time()

            with lock:
                if now - cache["timestamp"] < ttl:
                    return cache["value"]

                # Compute and update cache
                result = func(self, *args, **kwargs)
                cache["value"] = result
                cache["timestamp"] = now
                return result

        return wrapper
    return decorator


class SpotifyController:
    def __init__(self):
        super().__init__()

        self.osascript = subprocess.Popen(
            ["osascript", "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setpgrp
        )

    def _command(self, cmd):
        if not self.running():
            debug("SpotifyController._command: Spotify not running.")
            return

        script = f'''
tell application "Spotify"
    {cmd}
end tell
'''
        self.osascript.stdin.write(script + "\n")
        self.osascript.stdin.flush()

    @timed_cache(ttl=0.5)
    def status(self):
        """
            Returns Spotify playback status including position and track length.
            """
        script = '''
tell application "Spotify"
    if player state is stopped then
        return "stopped||0||0||0||0||"
    end if

    set stateStr to player state as string
    set pos to player position
    set dur to duration of current track
    set vol to sound volume
    set trackName to name of current track
    set artistName to artist of current track

    return stateStr & "|" & pos & "|" & dur & "|" & vol & "|" & trackName & "|" & artistName
end tell
'''

        result = {
                "state": "",
                "position_sec": 0.0,
                "duration_sec": 0.0,
                "volume": 0,
                "title": "",
                "artist": ""
        }

        if not self.running():
            debug("SpotifyController.status: Spotify not running.")
            return result

        try:
            result = subprocess.check_output(["osascript", "-e", script])
        except:
            return result
        decoded = result.decode().strip()
        state, pos, dur, vol, track, artist = decoded.split("|", 5)

        if pos:
            pos = float(pos.replace(",", "."))
        else:
            pos = None

        if dur:
            dur = float(dur.replace(",", ".")) / 1000
        else:
            dur = None

        if vol:
            vol = int(vol)
        else:
            vol = None

        return {
            "state": state,  # playing / paused / stopped
            "position": pos,  # current playback position
            "duration": dur,  # total track length
            "volume": vol,  # 0–100
            "title": track,
            "artist": artist
        }

    @timed_cache(ttl=0.5)
    def _get_running_state(self):
        script = '''
tell application "System Events"
    (name of processes) contains "Spotify"
end tell
'''
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )

        if result.stdout.strip() == "true":
            return True
        else:
            return False

    def running(self):
        return self._get_running_state()

    def get_currently_playing_title(self):
        return self.status().get("title", None)

    def get_currently_playing_artist(self):
        return self.status().get("artist", None)

    def get_currently_playing_position(self):
        return self.status().get("position", None)

    def get_currently_playing_duration(self):
        return self.status().get("duration", None)

    def get_playing_state(self):
        return self.status().get("state", None)

    def play(self):
        self._command("play")

    def pause(self):
        self._command("pause")

    def next(self):
        self._command("next track")

    def previous(self):
        self._command("previous track")

    @latest_value
    def seek(self, position):
        duration = self.get_currently_playing_duration()
        if duration is not None:
            new_position = position * duration
            self._command(f"set player position to {new_position}")

    @latest_value
    def set_volume(self, volume):
        self._command(f"set sound volume to {volume}")


class VLCController:
    """
    Control VLC via its HTTP (web) interface.
    Default URL works for local VLC with Web interface enabled.
    """
    def __init__(self, host="localhost", port=8080, password=""):
        super().__init__()
        self.base_url = f"http://{host}:{port}/requests"
        self.auth = HTTPBasicAuth("", password)

    # ---------- internal helpers ----------

    def _get(self, path, params=None):
        url = f"{self.base_url}/{path}"
        try:
            response = requests.get(url, params=params, auth=self.auth, timeout=2)
        except:
            return None
        return response

    def _command(self, cmd, **params):
        params["command"] = cmd
        try:
            self._get("status.xml", params)
        except Exception as e:
            error(f"Exception while communicating with VLC: {str(e)}")

    # ---------- playback control ----------

    def play(self):
        self._command("pl_play")

    def pause(self):
        self._command("pl_pause")

    def stop(self):
        self._command("pl_stop")

    def toggle(self):
        self._command("pl_pause")

    def next(self):
        self._command("pl_next")

    def previous(self):
        self._command("pl_previous")

    # ---------- volume ----------
    @latest_value
    def set_volume(self, volume):
        self._command("volume", val=volume)

    # ---------- seeking ----------
    @latest_value
    def seek(self, position):
        duration = self.get_currently_playing_duration()
        if duration is not None:
            new_position = position * duration
            self._command("seek", val=str(int(new_position)))

    # ---------- status ----------

    @timed_cache(ttl=0.5)
    def status(self):
        """
        Returns parsed playback status as a dictionary.
        """
        try:
            r = self._get("status.json")
            if r is None:
                return {}

            data = r.json()

            new_status = {
                "state": data.get("state"),                 # playing / paused / stopped
                "position": data.get("time"),               # seconds
                "position_rel": data.get("position"),
                "duration": data.get("length"),             # seconds
                "volume": data.get("volume"),               # 0–512
                "rate": data.get("rate"),
                "title": data.get("information", {})
                                .get("category", {})
                                .get("meta", {})
                                .get("title"),
                "artist": data.get("information", {})
                                 .get("category", {})
                                 .get("meta", {})
                                 .get("artist"),
                "filename": data.get("information", {})
                                   .get("category", {})
                                   .get("meta", {})
                                   .get("filename"),
            }
            return new_status
        except Exception as e:
            error(f"Exception while communicating with VLC: {str(e)}")
        return {}

    def get_currently_playing_title(self):
        return self.status().get("title", None)

    def get_currently_playing_artist(self):
        return self.status().get("artist", None)

    def get_currently_playing_position(self):
        return self.status().get("position", None)

    def get_currently_playing_position_rel(self):
        return self.status().get("position_rel", None)

    def get_currently_playing_duration(self):
        return self.status().get("duration", None)

    def get_playing_state(self):
        return self.status().get("state", None)

    # ---------- playback modes ----------

    # def set_repeat(self, enabled=True):
    #     self._command("pl_repeat")
    #     if not enabled:
    #         self._command("pl_repeat")
    #
    # def set_loop(self, enabled=True):
    #     self._command("pl_loop")
    #     if not enabled:
    #         self._command("pl_loop")
    #
    # def set_random(self, enabled=True):
    #     self._command("pl_random")
    #     if not enabled:
    #         self._command("pl_random")
    #
    # # ---------- playlist ----------
    #
    # def clear_playlist(self):
    #     self._command("pl_empty")
    #
    # def play_item(self, item_id):
    #     self._command("pl_play", id=item_id)


class SystemController:
    def __init__(self):
        super().__init__()

        self.osascript = subprocess.Popen(
            ["osascript", "-i"],
            stdin=subprocess.PIPE,
            text=True
        )

    def _command(self, cmd):
        script = f'''
{cmd}
'''
        self.osascript.stdin.write(script + "\n")
        self.osascript.stdin.flush()

    @latest_value
    def set_volume(self, volume):
        self._command(f"set volume output volume {volume}")