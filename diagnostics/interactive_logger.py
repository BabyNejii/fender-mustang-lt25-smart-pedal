import time
import sys
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from luma.core.interface.serial import i2c as luma_i2c
from luma.oled.device import sh1106 as luma_sh1106
from ltamp import LtAmp
from ltamp.protocol import _msg, CurrentPresetRequest
from ltamp.protocol.LoadPreset_pb2 import LoadPreset

SWITCH_PINS = [17, 27, 22, 23, 5]
TUNER_PIN = 6
ENCODER_SW = 12
ENCODER_CLK = 24
ENCODER_DT = 25

ALL_PINS = SWITCH_PINS + [TUNER_PIN, ENCODER_SW, ENCODER_CLK, ENCODER_DT]

PIN_NAMES = {
    17: "Footswitch 1",
    27: "Footswitch 2",
    22: "Footswitch 3",
    23: "Footswitch 4",
    5:  "Footswitch 5",
    6:  "Switch 6 (Tuner)",
    12: "Rotary Push (SW)",
    24: "Rotary CLK",
    25: "Rotary DT"
}

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

print("=== STARTING LIVE INTERACTIVE LOGGER ===")
sys.stdout.flush()

# 1. Connect to OLED
try:
    serial = luma_i2c(port=1, address=0x3C)
    oled = luma_sh1106(serial, width=128, height=64)
    font_colossal = ImageFont.truetype("/home/pi/font_stage.ttf", 64)
    font_name = ImageFont.truetype("/home/pi/font_stage.ttf", 16)
    font_name_sm = ImageFont.truetype("/home/pi/font_stage.ttf", 13)
    has_oled = True
    print("[OLED] Connected successfully.")
except Exception as e:
    has_oled = False
    print(f"[OLED] Failed: {e}")
sys.stdout.flush()

def update_oled(preset_idx):
    if not has_oled:
        return
    try:
        im = Image.new("1", (128, 64), 0)
        draw = ImageDraw.Draw(im)
        preset_num = f"{preset_idx + 1:02d}"
        bbox = draw.textbbox((0, 0), preset_num, font=font_colossal)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        nx = (58 - tw) // 2 - bbox[0]
        ny = (64 - th) // 2 - bbox[1]
        draw.text((nx, ny), preset_num, font=font_colossal, fill=255)
        draw.line((61, 4, 61, 60), fill=255)
        
        p_name = PRESET_NAMES[preset_idx] if preset_idx < len(PRESET_NAMES) else f"Preset {preset_idx+1}"
        words = p_name.strip().split()
        if len(words) == 1:
            lines = [words[0], ""]
        elif len(words) == 2:
            lines = [words[0], words[1]]
        else:
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        f = font_name if max(len(lines[0]), len(lines[1])) <= 7 else font_name_sm
        if lines[1]:
            draw.text((65, 12), lines[0], font=f, fill=255)
            draw.text((65, 34), lines[1], font=f, fill=255)
        else:
            draw.text((65, 23), lines[0], font=f, fill=255)
        oled.display(im)
    except Exception as e:
        print(f"[OLED Error]: {e}")

# 2. Connect to Amp
amp = LtAmp()
try:
    amp.connect()
    amp.send_sync_begin()
    time.sleep(0.05)
    amp.send_sync_end()
    time.sleep(0.1)
    cp = amp.request_current_preset()
    current_preset = cp.get("index", 1) - 1
    print(f"[AMP] Connected! Amp current slot is: {current_preset + 1} ({PRESET_NAMES[current_preset]})")
    update_oled(current_preset)
except Exception as e:
    print(f"[AMP] Connect failed: {e}")
    current_preset = 0
sys.stdout.flush()

def change_amp_preset(slot_1based):
    try:
        # 1. Send LoadPreset
        amp.set_preset(slot_1based)
        # 2. Send CurrentPresetRequest to FORCE amp LCD screen to redraw!
        amp.send_message(_msg(currentPresetRequest=CurrentPresetRequest(request=True)))
        print(f"[AMP COMMAND SENT] Slot {slot_1based} ({PRESET_NAMES[slot_1based - 1]}) [LoadPreset + Redraw Request]")
        sys.stdout.flush()
    except Exception as e:
        print(f"[AMP COMMAND ERROR] {e}")
        sys.stdout.flush()

# 3. Setup GPIO
GPIO.setmode(GPIO.BCM)
for p in ALL_PINS:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_clk = GPIO.input(ENCODER_CLK)
last_pin_val = {p: GPIO.input(p) for p in ALL_PINS}

print("\n>>> LOGGER IS LIVE! Press any footswitch or turn the rotary knob now! <<<\n")
sys.stdout.flush()

start_time = time.time()
while time.time() - start_time < 45:
    now = time.time()
    
    # Check encoder
    clk = GPIO.input(ENCODER_CLK)
    dt = GPIO.input(ENCODER_DT)
    if clk != last_clk and clk == GPIO.LOW:
        direction = +1 if dt != clk else -1
        current_preset = (current_preset + direction + 60) % 60
        print(f"[EVENT] ROTARY ENCODER TURNED: {'CW (+1)' if direction > 0 else 'CCW (-1)'} -> New Slot: {current_preset + 1} ({PRESET_NAMES[current_preset]})")
        update_oled(current_preset)
        change_amp_preset(current_preset + 1)
        sys.stdout.flush()
    last_clk = clk

    # Check all pins for state changes
    for p in ALL_PINS:
        val = GPIO.input(p)
        if val != last_pin_val[p]:
            name = PIN_NAMES.get(p, f"Pin {p}")
            if val == GPIO.LOW:
                print(f"[EVENT] {name} (Pin {p}) -> PRESSED (LOW)")
                if p in SWITCH_PINS:
                    slot_idx = SWITCH_PINS.index(p) + 1  # Bank 1: 1-5
                    current_preset = slot_idx - 1
                    print(f"        -> Triggering Switch {slot_idx} -> Slot {slot_idx} ({PRESET_NAMES[current_preset]})")
                    update_oled(current_preset)
                    change_amp_preset(slot_idx)
                elif p == TUNER_PIN:
                    print(f"        -> Tuner Switch 6 Pressed!")
                elif p == ENCODER_SW:
                    print(f"        -> Rotary Knob Clicked!")
            else:
                print(f"[EVENT] {name} (Pin {p}) -> RELEASED (HIGH)")
            last_pin_val[p] = val
            sys.stdout.flush()

    time.sleep(0.002)

print("\n=== LOGGER FINISHED ===")
try:
    amp.disconnect()
except:
    pass
GPIO.cleanup()
