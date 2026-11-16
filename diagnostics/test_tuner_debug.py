import time
import ltamp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState

amp = ltamp.LtAmp(debug=True)
amp.connect()

print("\n--- Sending TUNER_ENABLE with sync wrap ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_ENABLE, state=ModalState.OK)))
time.sleep(0.05)
amp.send_sync_end()
time.sleep(2.0)

print("\n--- Sending TUNER_DISABLE with sync wrap ---")
amp.send_sync_begin()
time.sleep(0.05)
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_DISABLE, state=ModalState.OK)))
time.sleep(0.05)
amp.send_sync_end()
time.sleep(1.0)

amp.disconnect()
