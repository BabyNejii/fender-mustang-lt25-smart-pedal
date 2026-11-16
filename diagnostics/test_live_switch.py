import time
import ltamp

print("Connecting to LT25...")
amp = ltamp.LtAmp()
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

print(">>> [TEST 1] Sending Slot 1 (Fender Clean)...")
amp.set_preset(1)
print("Slot 1 packet sent! Waiting 4 seconds...")
time.sleep(4)

print(">>> [TEST 2] Sending Slot 2 (Silky Solo)...")
amp.set_preset(2)
print("Slot 2 packet sent! Waiting 4 seconds...")
time.sleep(4)

print(">>> [TEST 3] Sending Slot 3 (Chicago Blues)...")
amp.set_preset(3)
print("Slot 3 packet sent! Waiting 4 seconds...")
time.sleep(4)

print("Test complete. Disconnecting.")
amp.disconnect()
