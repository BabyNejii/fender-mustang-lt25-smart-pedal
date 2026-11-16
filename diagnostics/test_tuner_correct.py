import time
import ltamp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState

amp = ltamp.LtAmp(debug=True)
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

print("\n--- Enabling Tuner (Handshake done, no sync wrap around tuner) ---")
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_ENABLE, state=ModalState.OK)))
time.sleep(4)

print("\n--- Disabling Tuner ---")
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_DISABLE, state=ModalState.OK)))
time.sleep(1)

amp.disconnect()
print("Done.")
