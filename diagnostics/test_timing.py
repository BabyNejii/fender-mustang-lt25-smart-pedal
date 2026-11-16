import time
import ltamp
from ltamp.protocol import _msg, CurrentPresetRequest

amp = ltamp.LtAmp(debug=True)
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

print("\n--- TEST: set_preset(4) ALONE ---")
amp.set_preset(4)
time.sleep(1.0)

print("\n--- TEST: set_preset(1) + currentPresetRequest ---")
amp.set_preset(1)
amp.send_message(_msg(currentPresetRequest=CurrentPresetRequest(request=True)))
time.sleep(2.0)

amp.disconnect()
