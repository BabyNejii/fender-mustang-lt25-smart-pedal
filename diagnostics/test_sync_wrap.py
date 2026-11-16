import time
import ltamp

print("Connecting to LT25...")
amp = ltamp.LtAmp()
amp.connect()

print("\n--- Test A: Sync Begin -> set_preset(2) -> Sync End (HID still OPEN) ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.set_preset(2)
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.2)
cp = amp.request_current_preset()
print("Slot read from amp while HID is open:", cp.get("index"))

print("\n--- Test B: Sync Begin -> set_preset(3) -> Sync End (HID still OPEN) ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.set_preset(3)
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.2)
cp = amp.request_current_preset()
print("Slot read from amp while HID is open:", cp.get("index"))

print("\nDisconnecting...")
amp.disconnect()
print("Disconnected.")
