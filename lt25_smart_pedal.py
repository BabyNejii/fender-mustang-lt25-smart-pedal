#!/usr/bin/env python3
"""
Fender Mustang LT25 Ultimate 6-Button Smart Footswitch Controller
Features:
- 12 Banks x 5 Presets (60 Presets total)
- Instant stomp down: Zero-latency preset 1-5 selection in current bank
- Press-again on active preset: Toggle Solo Boost (+3dB) with full-screen inversion
- Hold Switch 1 (>600ms): Bank Down
- Hold Switch 5 (>600ms): Bank Up
- Hold Switch 3 (>1000ms): Toggle Preset Mode <-> Stompbox Mode
- Dedicated Upper-Deck Tuner / Mute switch (Switch 6) with Any-Key Exit
- Rotary Encoder (Scroll seamlessly through all 60 presets, push to toggle mode)
- 1.3" I2C SH1106 / SSD1306 OLED Stage Display (Big Colossal Number + Clean Title)
- WS2812B RGB LED status indicators (Emerald Green / Fiery Red / Cyan / Amber)
- USB HID communication using ltamp protocol with SYNC handshake, Redraw request & keepalive
"""

import time
import json
import threading
import logging
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import board
import busio
import adafruit_ssd1306
try:
    from luma.core.interface.serial import i2c as luma_i2c
    from luma.oled.device import sh1106 as luma_sh1106
    HAS_LUMA = True
except ImportError:
    HAS_LUMA = False
from rpi_ws281x import PixelStrip, Color

# Fender LT Protocol Imports
from ltamp import LtAmp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState, CurrentPresetRequest
from ltamp.protocol.LoadPreset_pb2 import LoadPreset
from ltamp.protocol.SetDspUnitParameter_pb2 import SetDspUnitParameter

# --- CONFIGURATION ---
FENDER_VID = 0x1ed8
FENDER_PID = 0x0037
TOTAL_PRESETS = 60
BANK_SIZE = 5
TOTAL_BANKS = TOTAL_PRESETS // BANK_SIZE  # 12 Banks

# GPIO Assignments (BCM)
SWITCH_PINS = [17, 27, 22, 23, 5]  # Lower row preset switches 1 to 5
TUNER_SWITCH_PIN = 6               # Upper deck dedicated MUTE/TUNER switch (Switch 6)
ENCODER_CLK = 24                   # Rotary Encoder Channel A (CLK)
ENCODER_DT  = 25                   # Rotary Encoder Channel B (DT)
ENCODER_SW  = 12                   # Rotary Encoder Push Button (SW)
LED_COUNT = 6                      # 5 Lower LEDs + 1 Tuner LED
LED_PIN = 18                       # GPIO 18 (PWM0)
LED_BRIGHTNESS = 180               # 0 to 255

HOLD_BANK_TIME_SEC = 0.60    # 600ms for Bank Up/Down
HOLD_MODE_TIME_SEC = 1.00    # 1.0s for Mode Toggle
DEBOUNCE_TIME_SEC = 0.010    # 10ms fast software debounce

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- COLOR DEFINITIONS ---
COLOR_OFF    = Color(0, 0, 0)
COLOR_DIM    = Color(15, 15, 15)
COLOR_ACTIVE = Color(0, 255, 60)    # Emerald Green
COLOR_BOOST  = Color(255, 0, 0)     # Fiery Red
COLOR_BANK   = Color(0, 150, 255)   # Cyan
COLOR_STOMP  = Color(255, 120, 0)   # Amber

# --- PRESET NAMES DATABASE (Verified from amplifier memory) ---
PRESET_NAMES = [
    "Fender Clean", "Silky Solo", "Chicago Blues", "Classic Rock", "Dreamy",
    "Country Picking", "Skate Punk", "Solo Midboost", "Jazz Amp", "Brit 64 Rhythm",
    "Metal Lead", "Vintage Tremolo", "Super Dryclean", "Thrash Overkill", "Clean Delay",
    "Octobot 1 Note", "Little Champ", "Phaser Swirl", "60s Fuzz", "Mythic Crunch",
    "Touch Wah", "Super Rock", "Nice Flanger", "Vibra Doom", "Surf Music",
    "Blues Lead", "Rock A Billy", "Garage Fuzz", "Space Travel", "Acoustic Sim",
    "Empty 31", "Empty 32", "Empty 33", "Empty 34", "Empty 35",
    "Empty 36", "Empty 37", "Empty 38", "Empty 39", "Empty 40",
    "Empty 41", "Empty 42", "Empty 43", "Empty 44", "Empty 45",
    "Empty 46", "Empty 47", "Empty 48", "Empty 49", "Empty 50",
    "Empty 51", "Empty 52", "Empty 53", "Empty 54", "Classic Rock",
    "Nirv", "LP", "Enter Sandman", "Clean", "Back In Black"
]


class OLEDDisplay:
    """Handles 1.3-inch (SH1106 or SSD1306) I2C OLED display rendering."""
    def __init__(self):
        self.available = False
        self.device = None
        self.is_luma = False

        # 1. Try luma.oled SH1106 (standard driver for 1.3" 128x64 OLEDs)
        if HAS_LUMA:
            try:
                serial = luma_i2c(port=1, address=0x3C)
                self.device = luma_sh1106(serial, width=128, height=64)
                self.is_luma = True
                self.available = True
                logging.info("1.3\" SH1106 OLED initialized via luma.oled.")
            except Exception as e_luma:
                logging.warning(f"luma.oled SH1106 failed: {e_luma}")

        # 2. Fallback to Adafruit SSD1306 if luma not available
        if not self.available:
            try:
                i2c = busio.I2C(board.SCL, board.SDA)
                self.device = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
                self.device.fill(0)
                self.device.show()
                self.is_luma = False
                self.available = True
                logging.info("1.3\" SSD1306 OLED initialized via adafruit_ssd1306.")
            except Exception as e_ada:
                logging.warning(f"SSD1306 fallback failed: {e_ada}")

        if self.available:
            self.font_main = ImageFont.load_default()
            font_path = "/home/pi/font_stage.ttf"
            try:
                self.font_colossal = ImageFont.truetype(font_path, 64)
                self.font_name = ImageFont.truetype(font_path, 16)
                self.font_name_sm = ImageFont.truetype(font_path, 13)
                self.font_sm = ImageFont.truetype(font_path, 10)
                self.font_micro = ImageFont.truetype(font_path, 9)
                self.has_ttf = True
            except Exception as e_font:
                logging.warning(f"Could not load TrueType font: {e_font}, using default.")
                self.font_colossal = self.font_main
                self.font_name = self.font_main
                self.font_name_sm = self.font_main
                self.font_sm = self.font_main
                self.font_micro = self.font_main
                self.has_ttf = False
            self.clear()

    def clear(self):
        if not self.available:
            return
        if self.is_luma:
            self.device.clear()
        else:
            self.device.fill(0)
            self.device.show()

    def _show_image(self, image):
        if not self.available:
            return
        try:
            if self.is_luma:
                self.device.display(image)
            else:
                self.device.image(image)
                self.device.show()
        except Exception as e:
            logging.error(f"OLED show_image failed: {e}")

    def render(self, bank_idx: int, preset_idx: int, mode: str, is_boost: bool = False, stomp_states=None):
        if not self.available:
            return

        image = Image.new("1", (128, 64), 0)
        draw = ImageDraw.Draw(image)

        if mode == "TUNER":
            # Tuner / Amp Mute Screen
            draw.rectangle((0, 0, 128, 14), fill=255)
            draw.text((8, 1), "*** CHROMATIC TUNER ***", font=self.font_sm, fill=0)
            draw.rectangle((8, 20, 120, 46), outline=255, fill=255)
            draw.text((24, 25), "AMP MUTED", font=self.font_name, fill=0)
            draw.text((12, 51), "Tap any switch to exit", font=self.font_micro, fill=255)
        else:
            # 1. Left Half: Massive 64pt Colossal Preset Number (Full Screen Height, X=0..58)
            preset_num_str = f"{preset_idx + 1:02d}"
            bbox = draw.textbbox((0, 0), preset_num_str, font=self.font_colossal)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            nx = (58 - tw) // 2 - bbox[0]
            ny = (64 - th) // 2 - bbox[1]
            draw.text((nx, ny), preset_num_str, font=self.font_colossal, fill=255)

            # 2. Sleek Vertical Divider
            draw.line((61, 4, 61, 60), fill=255)

            # 3. Right Half: Preset Name on 2 Clean Rows (X=65..127) - Just the Title!
            if mode == "PRESET":
                p_name = PRESET_NAMES[preset_idx] if preset_idx < len(PRESET_NAMES) else f"Preset {preset_idx + 1}"
                words = p_name.strip().split()
                if len(words) == 1:
                    lines = [words[0], ""]
                elif len(words) == 2:
                    lines = [words[0], words[1]]
                else:
                    mid = len(words) // 2
                    lines = [" ".join(words[:mid]), " ".join(words[mid:])]

                max_len = max(len(lines[0]), len(lines[1]))
                f = self.font_name if max_len <= 7 else (self.font_name_sm if max_len <= 11 else self.font_micro)

                if lines[1]:
                    draw.text((65, 12), lines[0], font=f, fill=255)
                    draw.text((65, 34), lines[1], font=f, fill=255)
                else:
                    draw.text((65, 23), lines[0], font=f, fill=255)
            else:  # STOMP mode
                stomp_names = ["OD", "MOD", "DLY", "TAP", "REV"]
                coords = [(65, 6), (65, 24), (65, 42), (97, 6), (97, 24)]
                states = stomp_states or [False] * 5
                for i, name in enumerate(stomp_names):
                    x, y = coords[i]
                    is_on = states[i] if i < len(states) else False
                    if is_on:
                        draw.rectangle((x, y, x + 28, y + 14), outline=255, fill=255)
                        draw.text((x + 3, y + 2), name, font=self.font_micro, fill=0)
                    else:
                        draw.rectangle((x, y, x + 28, y + 14), outline=255, fill=0)
                        draw.text((x + 3, y + 2), name, font=self.font_micro, fill=255)

        # High-visibility visual feedback: Invert entire display when Solo Boost is active
        if is_boost and mode != "TUNER":
            image = ImageOps.invert(image.convert("L")).convert("1")

        self._show_image(image)


class SmartPedalController:
    def __init__(self):
        self.amp = None
        self.current_bank = 0      # 0 to 11
        self.current_preset = 0    # 0 to 59
        self.mode = "PRESET"       # "PRESET" or "STOMP"
        self.boost_active = False  # Press-again Solo Boost (+3dB)
        self.base_amp_volume = -12.0
        self.last_tap_time = 0.0
        self.stomp_states = [False] * 5
        self.tuner_active = False

        self.display = OLEDDisplay()
        self.strip = PixelStrip(LED_COUNT, LED_PIN, 800000, 10, False, LED_BRIGHTNESS)
        self.strip.begin()

        self.lock = threading.Lock()
        self._sync_in_progress = False
        
        # Connect to amp and synchronize state
        self.connect_amp()
        self.update_hardware()

    def trigger_dsp_sync(self):
        """Asynchronously query preset DSP parameters (base volume & stomp bypasses) without blocking the UI."""
        if getattr(self, '_sync_in_progress', False):
            return
        self._sync_in_progress = True
        def _worker():
            try:
                time.sleep(0.05)
                self.sync_preset_dsp_state()
            finally:
                self._sync_in_progress = False
        threading.Thread(target=_worker, daemon=True).start()

    def sync_preset_dsp_state(self):
        """Inspects current active preset audioGraph: caches base volume for Solo Boost and syncs stomp states."""
        try:
            cp = self.amp.request_current_preset()
            if not cp or not cp.get("data"):
                return
            pdata = json.loads(cp["data"])
            nodes = pdata.get("audioGraph", {}).get("nodes", [])
            nodes_by_id = {n.get("nodeId"): n for n in nodes}

            if "amp" in nodes_by_id:
                self.base_amp_volume = nodes_by_id["amp"].get("dspUnitParameters", {}).get("volume", -12.0)

            def is_node_active(node_name):
                n = nodes_by_id.get(node_name)
                if not n or n.get("FenderId") == "DUBS_Passthru":
                    return False
                return not n.get("dspUnitParameters", {}).get("bypass", False)

            self.stomp_states[0] = is_node_active("stomp")
            self.stomp_states[1] = is_node_active("mod")
            self.stomp_states[2] = is_node_active("delay")
            self.stomp_states[3] = (nodes_by_id.get("delay", {}).get("FenderId") != "DUBS_Passthru")
            self.stomp_states[4] = is_node_active("reverb")
            logging.info(f"DSP Synced: OD={self.stomp_states[0]}, MOD={self.stomp_states[1]}, DLY={self.stomp_states[2]}, REV={self.stomp_states[4]}, BaseVol={self.base_amp_volume:.1f}dB")
        except Exception as e:
            logging.warning(f"Could not sync DSP states: {e}")

    def apply_solo_boost(self, enable: bool):
        """Applies a true +3.0 dB volume boost directly to the amp's DSP stage."""
        if not self.connect_amp():
            return
        with self.lock:
            if not self.amp:
                return
            try:
                target_vol = (self.base_amp_volume + 3.0) if enable else self.base_amp_volume
                self.amp.send_sync_begin()
                self.amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="amp", parameterId="volume", floatParameter=target_vol)))
                self.amp.send_sync_end()
                logging.info(f"Solo Boost {'ENGAGED' if enable else 'DISENGAGED'}: Amp Volume = {target_vol:.2f} dB (Base: {self.base_amp_volume:.2f} dB)")
            except Exception as e:
                logging.error(f"Failed to apply solo boost: {e}")

    def connect_amp(self) -> bool:
        with self.lock:
            if self.amp and self.amp.device:
                return True
            try:
                amp = LtAmp()
                if not amp.find_amp():
                    return False
                amp.connect()
                # Handshake is mandatory for LT25 to accept commands
                amp.send_sync_begin()
                time.sleep(0.05)
                amp.send_sync_end()
                time.sleep(0.05)
                self.amp = amp
                logging.info("Connected to Fender Mustang LT25 via USB HID (Sync complete).")

                # Synchronize with amplifier's current active preset
                try:
                    cp = self.amp.request_current_preset()
                    amp_slot = cp.get("index")
                    if amp_slot and 1 <= amp_slot <= TOTAL_PRESETS:
                        self.current_preset = amp_slot - 1
                        self.current_bank = self.current_preset // BANK_SIZE
                        logging.info(f"Synchronized with Fender LT25: Slot {amp_slot} ({PRESET_NAMES[self.current_preset]})")
                except Exception as e:
                    logging.warning(f"Could not read current preset from amp during connect: {e}")
                self.sync_preset_dsp_state()
                return True
            except Exception as e:
                logging.warning(f"Failed to connect to Fender LT25: {e}")
                if self.amp:
                    try:
                        self.amp.disconnect()
                    except Exception:
                        pass
                self.amp = None
                return False

    def send_preset_to_amp(self, preset_idx: int):
        if not self.connect_amp():
            logging.warning("Cannot send preset; Amp disconnected.")
            return

        # Physical Mustang LT presets are 1-indexed (1 to 60)
        slot_idx = (preset_idx % TOTAL_PRESETS) + 1
        with self.lock:
            if not self.amp:
                return
            try:
                # Fender LT25 Transactional Protocol: Every preset change MUST be wrapped in SYNC_BEGIN / SYNC_END
                self.amp.send_sync_begin()
                self.amp.set_preset(slot_idx)
                self.amp.send_sync_end()
                logging.info(f"Fender LT25 switched to slot {slot_idx} ({PRESET_NAMES[preset_idx % TOTAL_PRESETS]})")
            except Exception as e:
                logging.error(f"HID write failed: {e}")
                try:
                    self.amp.disconnect()
                except Exception:
                    pass
                self.amp = None
        self.trigger_dsp_sync()

    def update_hardware(self):
        # Update OLED
        self.display.render(self.current_bank, self.current_preset, self.mode, self.boost_active, self.stomp_states)

        # Update WS2812B LEDs
        active_in_bank = self.current_preset % BANK_SIZE
        current_preset_bank = self.current_preset // BANK_SIZE

        for i in range(LED_COUNT):
            if self.mode == "TUNER":
                # In Tuner mode: LED 6 (index 5) lights up green, others off
                self.strip.setPixelColor(i, COLOR_ACTIVE if i == 5 else COLOR_OFF)
            elif self.mode == "PRESET":
                if i == 5:
                    # Tuner LED is dim off when not in tuner mode
                    self.strip.setPixelColor(5, COLOR_OFF)
                elif current_preset_bank == self.current_bank and i == active_in_bank:
                    # Fiery Red when Boost is ON, Emerald Green when Normal
                    self.strip.setPixelColor(i, COLOR_BOOST if self.boost_active else COLOR_ACTIVE)
                else:
                    self.strip.setPixelColor(i, COLOR_DIM)
            else:  # STOMP mode
                if i == 5:
                    self.strip.setPixelColor(5, COLOR_OFF)
                else:
                    is_on = self.stomp_states[i] if i < len(self.stomp_states) else False
                    self.strip.setPixelColor(i, COLOR_STOMP if is_on else COLOR_DIM)
        self.strip.show()

    def flash_bank_change(self):
        for _ in range(2):
            for i in range(LED_COUNT):
                self.strip.setPixelColor(i, COLOR_BANK)
            self.strip.show()
            time.sleep(0.08)
            for i in range(LED_COUNT):
                self.strip.setPixelColor(i, COLOR_OFF)
            self.strip.show()
            time.sleep(0.08)

    # --- ACTION HANDLERS ---
    def start_watchdog(self):
        """Background thread: reconnects if amp is power cycled or cable bumped."""
        def watchdog_loop():
            while True:
                time.sleep(3.0)
                if not self.amp or not self.amp.device:
                    if self.connect_amp():
                        logging.info("Amp Hotplug Watchdog: Automatically reconnected to Fender LT25!")
                        self.send_preset_to_amp(self.current_preset)
                        self.update_hardware()
        t = threading.Thread(target=watchdog_loop, daemon=True)
        t.start()

    def select_preset_slot(self, slot_in_bank: int):
        target_preset = (self.current_bank * BANK_SIZE) + slot_in_bank
        # Press-Again Behavior: If already active, toggle Solo Boost!
        if self.current_preset == target_preset and self.mode == "PRESET":
            self.boost_active = not self.boost_active
            self.apply_solo_boost(self.boost_active)
        else:
            self.boost_active = False
            self.current_preset = target_preset
            self.send_preset_to_amp(self.current_preset)
        self.update_hardware()

    def toggle_tuner(self):
        self.tuner_active = not getattr(self, 'tuner_active', False)
        logging.info(f"Mute / Tuner Mode: {'ENGAGED' if self.tuner_active else 'DISENGAGED'}")

        # Always reset Solo Boost when toggling tuner so volume returns cleanly to normal preset level
        if self.boost_active:
            self.boost_active = False
            self.apply_solo_boost(False)

        if self.tuner_active:
            self.mode_backup = self.mode
            self.mode = "TUNER"
            self.update_hardware()

            if self.connect_amp():
                with self.lock:
                    if self.amp:
                        try:
                            # TUNER_ENABLE initiates tuner modal directly
                            self.amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_ENABLE, state=ModalState.OK)))
                        except Exception as e:
                            logging.error(f"Failed to send tuner modal: {e}")
                            try:
                                self.amp.disconnect()
                            except Exception:
                                pass
                            self.amp = None
        else:
            self.mode = getattr(self, 'mode_backup', 'PRESET')
            self.update_hardware()

            if self.connect_amp():
                with self.lock:
                    if self.amp:
                        try:
                            # Transactional exit: TUNER_DISABLE MUST be wrapped in SYNC_BEGIN / SYNC_END for the LT25 firmware to unmute!
                            self.amp.send_sync_begin()
                            self.amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_DISABLE, state=ModalState.OK)))
                            self.amp.send_sync_end()
                        except Exception as e:
                            logging.error(f"Failed to exit tuner modal: {e}")
                            try:
                                self.amp.disconnect()
                            except Exception:
                                pass
                            self.amp = None

    def encoder_rotate(self, direction: int):
        if self.tuner_active:
            self.toggle_tuner()
        # Seamlessly cycle through ALL 60 PRESETS
        self.current_preset = (self.current_preset + direction + TOTAL_PRESETS) % TOTAL_PRESETS
        self.current_bank = self.current_preset // BANK_SIZE
        self.boost_active = False
        self.send_preset_to_amp(self.current_preset)
        self.update_hardware()

    def bank_up(self):
        if self.tuner_active:
            self.toggle_tuner()
        self.current_bank = (self.current_bank + 1) % TOTAL_BANKS
        self.current_preset = self.current_bank * BANK_SIZE
        logging.info(f"Bank Up: Now at Bank {self.current_bank + 1} (Preset {self.current_preset + 1})")
        self.flash_bank_change()
        self.send_preset_to_amp(self.current_preset)
        self.update_hardware()

    def bank_down(self):
        if self.tuner_active:
            self.toggle_tuner()
        self.current_bank = (self.current_bank - 1 + TOTAL_BANKS) % TOTAL_BANKS
        self.current_preset = self.current_bank * BANK_SIZE
        logging.info(f"Bank Down: Now at Bank {self.current_bank + 1} (Preset {self.current_preset + 1})")
        self.flash_bank_change()
        self.send_preset_to_amp(self.current_preset)
        self.update_hardware()

    def toggle_mode(self):
        if self.tuner_active:
            self.toggle_tuner()
        self.mode = "STOMP" if self.mode == "PRESET" else "PRESET"
        logging.info(f"Mode changed to: {self.mode}")
        self.update_hardware()

    def toggle_stomp(self, index: int):
        if index == 3:
            # Switch 4: Tap Tempo for delay
            now = time.time()
            if self.last_tap_time and (now - self.last_tap_time) < 2.0:
                interval = now - self.last_tap_time
                bpm = max(40.0, min(240.0, 60.0 / interval))
                logging.info(f"Tap Tempo: {bpm:.1f} BPM ({interval*1000:.0f}ms)")
                with self.lock:
                    if self.amp:
                        try:
                            self.amp.send_sync_begin()
                            self.amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="delay", parameterId="tapTimeBPM", floatParameter=bpm)))
                            self.amp.send_sync_end()
                        except Exception as e:
                            logging.error(f"Failed to set tap tempo: {e}")
            self.last_tap_time = now
            self.stomp_states[3] = True
            self.update_hardware()
            return

        node_map = {0: "stomp", 1: "mod", 2: "delay", 4: "reverb"}
        node_id = node_map.get(index)
        if not node_id:
            return

        self.stomp_states[index] = not self.stomp_states[index]
        is_active = self.stomp_states[index]
        is_bypassed = not is_active

        logging.info(f"STOMP Switch {index + 1}: {node_id.upper()} set to {'ACTIVE' if is_active else 'BYPASSED'}")
        if self.connect_amp():
            with self.lock:
                if self.amp:
                    try:
                        self.amp.send_sync_begin()
                        self.amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(
                            nodeId=node_id,
                            parameterId="bypass",
                            boolParameter=is_bypassed
                        )))
                        self.amp.send_sync_end()
                    except Exception as e:
                        logging.error(f"Failed to toggle DSP bypass for {node_id}: {e}")

        self.update_hardware()


def run_button_monitor(controller: SmartPedalController):
    GPIO.setmode(GPIO.BCM)
    all_switches = SWITCH_PINS + [TUNER_SWITCH_PIN, ENCODER_SW]
    for pin in all_switches:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Rotary Encoder Quadrature Setup
    GPIO.setup(ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    last_clk_state = GPIO.input(ENCODER_CLK)

    button_state = {pin: False for pin in all_switches}
    press_time = {pin: 0.0 for pin in all_switches}
    last_release_time = {pin: 0.0 for pin in all_switches}
    long_handled = {pin: False for pin in all_switches}

    logging.info("Button & Encoder Monitor loop started.")

    while True:
        now = time.time()

        # 1. Rotary Encoder Polling
        clk_state = GPIO.input(ENCODER_CLK)
        dt_state = GPIO.input(ENCODER_DT)
        if clk_state != last_clk_state and clk_state == GPIO.LOW:
            # Clock transitioned; check DT to determine direction
            direction = +1 if dt_state != clk_state else -1
            logging.info(f"Rotary Encoder: {'CW (+1)' if direction > 0 else 'CCW (-1)'}")
            controller.encoder_rotate(direction)
        last_clk_state = clk_state

        # 2. Footswitches & Push Button Polling
        for idx, pin in enumerate(all_switches):
            is_pressed = (GPIO.input(pin) == GPIO.LOW)

            # Button Pressed Down
            if is_pressed and not button_state[pin]:
                # Debounce lockout: Ignore contact chatter within 40ms of release
                if (now - last_release_time[pin]) < 0.040:
                    continue

                button_state[pin] = True
                press_time[pin] = now
                long_handled[pin] = False
                logging.info(f"Switch {idx + 1} (Pin {pin}) STOMPED DOWN")

                # Zero-latency response
                if controller.tuner_active:
                    # Stomping ANY button while in Tuner mode immediately closes tuner and returns to active preset!
                    controller.toggle_tuner()
                elif idx < 5 and controller.mode == "PRESET":
                    controller.select_preset_slot(idx)
                elif pin == TUNER_SWITCH_PIN:
                    # Instant Tuner Toggle on press down
                    controller.toggle_tuner()
                elif pin == ENCODER_SW:
                    # Instant Mode Toggle on encoder knob press
                    controller.toggle_mode()

            # Button Held Down (Check for long press on switches 1, 5, 3)
            elif is_pressed and button_state[pin] and not long_handled[pin]:
                duration = now - press_time[pin]

                # Switch 1 Held: Bank Down
                if idx == 0 and duration >= HOLD_BANK_TIME_SEC:
                    logging.info("Switch 1 long-press: BANK DOWN")
                    controller.bank_down()
                    long_handled[pin] = True

                # Switch 5 Held: Bank Up
                elif idx == 4 and duration >= HOLD_BANK_TIME_SEC:
                    logging.info("Switch 5 long-press: BANK UP")
                    controller.bank_up()
                    long_handled[pin] = True

                # Switch 3 Held: Mode Toggle
                elif idx == 2 and duration >= HOLD_MODE_TIME_SEC:
                    logging.info("Switch 3 long-press: MODE TOGGLE")
                    controller.toggle_mode()
                    long_handled[pin] = True

            # Button Released
            elif not is_pressed and button_state[pin]:
                # Debounce lockout: Ignore mechanical chatter within 40ms of press down
                if (now - press_time[pin]) < 0.040:
                    continue

                button_state[pin] = False
                last_release_time[pin] = now
                duration = now - press_time[pin]
                logging.info(f"Switch {idx + 1} (Pin {pin}) RELEASED ({duration*1000:.0f}ms)")

                if not long_handled[pin] and duration >= DEBOUNCE_TIME_SEC:
                    if idx < 5 and controller.mode == "STOMP" and not controller.tuner_active:
                        # In STOMP mode, toggle effect block on release
                        controller.toggle_stomp(idx)

        time.sleep(0.005)


def main():
    controller = SmartPedalController()
    controller.start_watchdog()
    run_button_monitor(controller)

if __name__ == "__main__":
    main()
