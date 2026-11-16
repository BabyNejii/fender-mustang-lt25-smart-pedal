import time
import ltamp
from ltamp.protocol import _msg, ModalStatusMessage, ModalContext, ModalState

print("Sending TUNER_ENABLE...")
amp = ltamp.LtAmp()
amp.connect()
amp.send_sync_begin()
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_ENABLE, state=ModalState.OK)))
amp.send_sync_end()
amp.disconnect()

print("Muted! Waiting 3 seconds...")
time.sleep(3.0)

print("Sending TUNER_DISABLE...")
amp = ltamp.LtAmp()
amp.connect()
amp.send_sync_begin()
amp.send_message(_msg(modalStatusMessage=ModalStatusMessage(context=ModalContext.TUNER_DISABLE, state=ModalState.OK)))
amp.send_sync_end()
amp.disconnect()
print("Unmuted!")
