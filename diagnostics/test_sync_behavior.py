import time
import ltamp

amp = ltamp.LtAmp(debug=True)
amp.connect()

print("\n--- TEST 1: sync_begin -> set_preset(7) -> sync_end ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.set_preset(7)
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.2)
cp1 = amp.request_current_preset()
print("Slot after Test 1:", cp1.get("index"))

print("\n--- TEST 2: set_preset(8) WITHOUT sync_begin/sync_end ---")
amp.set_preset(8)
time.sleep(0.2)
cp2 = amp.request_current_preset()
print("Slot after Test 2 (no sync):", cp2.get("index"))

print("\n--- TEST 3: sync_begin -> set_preset(9) -> sync_end ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.set_preset(9)
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.2)
cp3 = amp.request_current_preset()
print("Slot after Test 3:", cp3.get("index"))

amp.disconnect()
