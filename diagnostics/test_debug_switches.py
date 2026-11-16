import time
import ltamp

amp = ltamp.LtAmp(debug=True)
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

print("\n--- Sending set_preset(2) ---")
amp.set_preset(2)
time.sleep(1.0)

print("\n--- Sending set_preset(3) ---")
amp.set_preset(3)
time.sleep(1.0)

amp.disconnect()
