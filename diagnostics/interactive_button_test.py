import time
import sys
import RPi.GPIO as GPIO
import ltamp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c as luma_i2c
from luma.oled.device import sh1106 as luma_sh1106

TOTAL_PRESETS = 60
BANK_SIZE = 5
SWITCH_PINS = [17, 27, 22, 23, 5]
TUNER_SWITCH_PIN = 6
ENCODER_CLK = 24
ENCODER_DT = 25
ENCODER_SW = 12

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

print("Initializing OLED...")
try:
    serial = luma_i2c(port=1, address=0x3C)
    oled = luma_sh1106(serial, width=128, height=64)
    font_colossal = ImageFont.truetype("/home/pi/font_stage.ttf", 64)
    font_name = ImageFont.truetype("/home/pi/font_stage.ttf", 16)
    font_name_sm = ImageFont.truetype("/home/pi/font_stage.ttf", 13)
    has_oled = True
except Exception as e:
    print(f"OLED init failed: {e}")
    has_oled = False

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
        print(f"OLED render failed: {e}")

def send_preset_atomic(slot_1based):
    t0 = time.time()
    amp = ltamp.LtAmp()
    if not amp.find_amp():
        print(f"[ERROR] Amp not detected on USB!")
        return
    amp.connect()
    amp.send_sync_begin()
    amp.set_preset(slot_1based)
    amp.send_sync_end()
    amp.disconnect()
    elapsed = (time.time() - t0) * 1000
    print(f"[AMP] Successfully switched to Slot {slot_1based} ({PRESET_NAMES[slot_1based - 1]}) in {elapsed:.1f}ms")
    sys.stdout.flush()

# Check initial preset on amp
current_preset = 3  # default
try:
    amp = ltamp.LtAmp()
    if amp.find_amp():
        amp.connect()
        amp.send_sync_begin()
        amp.send_sync_end()
        cp = amp.request_current_preset()
        slot = cp.get("index")
        if slot and 1 <= slot <= TOTAL_PRESETS:
            current_preset = slot - 1
        amp.disconnect()
except Exception:
    pass

current_bank = current_preset // BANK_SIZE
update_oled(current_preset)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
all_pins = SWITCH_PINS + [TUNER_SWITCH_PIN, ENCODER_SW]
for p in all_pins:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_clk = GPIO.input(ENCODER_CLK)
btn_state = {p: False for p in all_pins}

print(f"\n=======================================================")
print(f"  INTERACTIVE TEST READY (Running for 30 seconds)")
print(f"  Current Amp Slot: {current_preset + 1} ({PRESET_NAMES[current_preset]})")
print(f"  STOMP ANY FOOTSWITCH (1-5) OR TURN THE ROTARY KNOB NOW!")
print(f"=======================================================\n")
sys.stdout.flush()

start_time = time.time()
while time.time() - start_time < 30:
    now = time.time()

    # Rotary Encoder
    clk = GPIO.input(ENCODER_CLK)
    dt = GPIO.input(ENCODER_DT)
    if clk != last_clk and clk == GPIO.LOW:
        direction = +1 if dt != clk else -1
        current_preset = (current_preset + direction + TOTAL_PRESETS) % TOTAL_PRESETS
        current_bank = current_preset // BANK_SIZE
        print(f"[KNOB TURN] Direction: {direction:+d} -> Slot {current_preset + 1}")
        update_oled(current_preset)
        send_preset_atomic(current_preset + 1)
    last_clk = clk

    # Footswitches
    for idx, p in enumerate(all_pins):
        is_low = (GPIO.input(p) == GPIO.LOW)
        if is_low and not btn_state[p]:
            btn_state[p] = True
            if idx < 5:
                slot_in_bank = idx
                target = (current_bank * BANK_SIZE) + slot_in_bank
                current_preset = target
                print(f"[STOMP] Footswitch {idx + 1} pressed -> Slot {target + 1} ({PRESET_NAMES[target]})")
                update_oled(current_preset)
                send_preset_atomic(target + 1)
            elif p == TUNER_SWITCH_PIN:
                print(f"[STOMP] Switch 6 (Tuner)")
            elif p == ENCODER_SW:
                print(f"[CLICK] Encoder push button")
        elif not is_low and btn_state[p]:
            btn_state[p] = False

    time.sleep(0.005)

print("\nInteractive test finished.")
