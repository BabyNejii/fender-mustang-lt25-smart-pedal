import sys
import time
import json
import ltamp

target = int(sys.argv[1]) if len(sys.argv) > 1 else 5

print(f"--- FENDER LT25 DIRECT PACKET TEST ---")
print(f"Target preset: Slot {target}")

amp = ltamp.LtAmp(debug=True)
amp.connect()
print("1. HID Connected.")

amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)
print("2. SYNC Handshake Completed.")

try:
    cp = amp.request_current_preset()
    idx = cp.get("index")
    data = json.loads(cp.get("data", "{}"))
    name = data.get("info", {}).get("displayName", "").strip()
    print(f"3. Amp reported current slot BEFORE change: {idx} ('{name}')")
except Exception as e:
    print(f"3. Could not read current preset: {e}")

print(f"\n4. >>> SENDING LoadPreset({target}) PACKET TO AMP <<<")
amp.set_preset(target)
print("Packet written to HID device.")

print("\n5. Holding HID connection open for 3 seconds...")
time.sleep(3.0)

try:
    cp2 = amp.request_current_preset()
    idx2 = cp2.get("index")
    data2 = json.loads(cp2.get("data", "{}"))
    name2 = data2.get("info", {}).get("displayName", "").strip()
    print(f"6. Amp reported slot AFTER change (while HID is open): {idx2} ('{name2}')")
except Exception as e:
    print(f"6. Could not verify new preset: {e}")

print("\n7. Closing HID device (amp.disconnect)...")
amp.disconnect()
print("8. Disconnected.")
