import time
import ltamp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState

amp = ltamp.LtAmp(debug=True)
amp.connect()

print("\n--- SENDING TUNER_ENABLE (Alone, no sync wrap) ---")
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_ENABLE, state=ModalState.OK)))
print("Sent TUNER_ENABLE! Holding for 5 seconds...")
time.sleep(5.0)

print("\n--- SENDING TUNER_DISABLE ---")
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_DISABLE, state=ModalState.OK)))
print("Sent TUNER_DISABLE!")
time.sleep(1.0)

amp.disconnect()
print("Disconnected.")
