import time
import ltamp
from ltamp.protocol import _msg
from ltamp.protocol.CurrentDisplayedPresetIndexStatus_pb2 import CurrentDisplayedPresetIndexStatus
from ltamp.protocol.CurrentLoadedPresetIndexStatus_pb2 import CurrentLoadedPresetIndexStatus
from ltamp.protocol.LoadPreset_pb2 import LoadPreset

amp = ltamp.LtAmp(debug=True)
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

target = 1  # Fender Clean (Slot 1)
print(f"--- Sending LoadPreset({target}) ---")
amp.set_preset(target)
time.sleep(0.2)

print(f"--- Sending CurrentDisplayedPresetIndexStatus({target}) ---")
try:
    msg1 = _msg(currentDisplayedPresetIndexStatus=CurrentDisplayedPresetIndexStatus(currentDisplayedPresetIndex=target))
    amp.send_message(msg1)
    print("Sent currentDisplayedPresetIndexStatus successfully")
except Exception as e:
    print("Failed currentDisplayedPresetIndexStatus:", e)
time.sleep(0.2)

print(f"--- Sending CurrentLoadedPresetIndexStatus({target}) ---")
try:
    msg2 = _msg(currentLoadedPresetIndexStatus=CurrentLoadedPresetIndexStatus(currentLoadedPresetIndex=target))
    amp.send_message(msg2)
    print("Sent currentLoadedPresetIndexStatus successfully")
except Exception as e:
    print("Failed currentLoadedPresetIndexStatus:", e)
time.sleep(0.2)

print("Current preset from amp:", amp.request_current_preset())
amp.disconnect()
print("Done.")
