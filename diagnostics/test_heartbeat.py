import time
import ltamp
from ltamp.protocol import _msg
from ltamp.protocol.Heartbeat_pb2 import Heartbeat

amp = ltamp.LtAmp(debug=True)
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

print("\n--- Sending Heartbeat ---")
amp.send_message(_msg(heartbeat=Heartbeat(dummyField=True)))
time.sleep(1.0)

amp.disconnect()
