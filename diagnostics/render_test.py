from PIL import Image, ImageDraw, ImageFont, ImageOps

font_huge = ImageFont.truetype('C:/Windows/Fonts/ARIALNB.TTF', 24)
font_med = ImageFont.truetype('C:/Windows/Fonts/ARIALNB.TTF', 13)
font_sm = ImageFont.truetype('C:/Windows/Fonts/ARIALNB.TTF', 10)
font_micro = ImageFont.truetype('C:/Windows/Fonts/ARIALNB.TTF', 9)

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

def render(bank_idx, preset_idx, mode, is_boost=False, stomp_states=None):
    image = Image.new("1", (128, 64), 0)
    draw = ImageDraw.Draw(image)

    if mode == "TUNER":
        draw.rectangle((0, 0, 128, 11), fill=255)
        draw.text((2, 0), "[TUNER] MUTE & TUNE", font=font_sm, fill=0)
        
        # Center Muted text
        draw.text((14, 20), "*** MUTED ***", font=font_huge, fill=255)
        
        # Footer
        draw.rectangle((2, 50, 126, 63), outline=255, fill=255)
        draw.text((8, 51), "TAP ANY SWITCH TO PLAY", font=font_sm, fill=0)

    elif mode == "STOMP":
        draw.rectangle((0, 0, 128, 11), fill=255)
        draw.text((2, 0), f"[STOMP] #{preset_idx + 1:02d}", font=font_sm, fill=0)
        draw.text((75, 0), f"BANK {bank_idx + 1:02d}/12", font=font_sm, fill=0)

        p_name = PRESET_NAMES[preset_idx] if preset_idx < len(PRESET_NAMES) else f"Preset {preset_idx + 1}"
        draw.text((4, 16), p_name[:16], font=font_med, fill=255)
        draw.text((4, 33), "STOMPBOX DIRECT ACCESS", font=font_micro, fill=255)

        stomp_names = ["OD", "MOD", "DLY", "TAP", "REV"]
        for i, name in enumerate(stomp_names):
            x = i * 25 + 2
            is_on = stomp_states[i] if stomp_states and i < len(stomp_states) else False
            if is_on:
                draw.rectangle((x - 1, 50, x + 21, 63), outline=255, fill=255)
                draw.text((x + 2, 51), name, font=font_micro, fill=0)
            else:
                draw.rectangle((x - 1, 50, x + 21, 63), outline=255, fill=0)
                draw.text((x + 2, 51), name, font=font_micro, fill=255)

    else: # PRESET mode
        # 1. Top Banner
        draw.rectangle((0, 0, 128, 11), fill=255)
        start_slot = (bank_idx * 5) + 1
        end_slot = start_slot + 4
        header_left = f"[PRESET] BANK {bank_idx + 1:02d}"
        header_right = f"({start_slot:02d}-{end_slot:02d})"
        draw.text((2, 0), header_left, font=font_sm, fill=0)
        draw.text((85, 0), header_right, font=font_sm, fill=0)

        # 2. Main Preset Center Section (Y=13..47)
        p_name = PRESET_NAMES[preset_idx] if preset_idx < len(PRESET_NAMES) else f"Preset {preset_idx + 1}"
        preset_num_str = f"{preset_idx + 1:02d}"

        # Big Number Box: 32px wide x 34px high solid white box with bold black numerals
        draw.rectangle((2, 13, 34, 47), outline=255, fill=255)
        bbox = draw.textbbox((0, 0), preset_num_str, font=font_huge)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        nx = 2 + (32 - tw) // 2 - bbox[0]
        ny = 13 + (34 - th) // 2 - bbox[1]
        draw.text((nx, ny), preset_num_str, font=font_huge, fill=0)

        # Right of box: Preset Name & Tone / Boost Status
        name_font = font_med if len(p_name) <= 12 else font_sm
        draw.text((38, 16), p_name[:15], font=name_font, fill=255)
        status_str = "★ SOLO BOOST" if is_boost else "STANDARD GAIN"
        draw.text((38, 33), status_str, font=font_micro, fill=255)

        # 3. Dynamic Switch Assignment Footer (Y=50..63)
        active_slot = preset_idx % 5
        for i in range(5):
            x = i * 25 + 2
            slot_num = f"{(bank_idx * 5) + i + 1:02d}"
            if i == active_slot and (preset_idx // 5 == bank_idx):
                draw.rectangle((x - 1, 50, x + 21, 63), outline=255, fill=255)
                draw.text((x + 3, 51), slot_num, font=font_sm, fill=0)
            else:
                draw.rectangle((x - 1, 50, x + 21, 63), outline=255, fill=0)
                draw.text((x + 3, 51), slot_num, font=font_sm, fill=255)

    if is_boost and mode != "TUNER":
        image = ImageOps.invert(image.convert("L")).convert("1")

    return image

render(0, 0, "PRESET", False).save("C:/Users/Ivo/Desktop/stuff/projects/MISC/amp-research/screen_preset_normal.png")
render(0, 0, "PRESET", True).save("C:/Users/Ivo/Desktop/stuff/projects/MISC/amp-research/screen_preset_boost.png")
render(0, 0, "TUNER").save("C:/Users/Ivo/Desktop/stuff/projects/MISC/amp-research/screen_tuner.png")
render(0, 0, "STOMP", stomp_states=[True, False, True, False, False]).save("C:/Users/Ivo/Desktop/stuff/projects/MISC/amp-research/screen_stomp.png")
render(11, 59, "PRESET", False).save("C:/Users/Ivo/Desktop/stuff/projects/MISC/amp-research/screen_preset_slot60.png")
print("Rendered test images successfully.")
