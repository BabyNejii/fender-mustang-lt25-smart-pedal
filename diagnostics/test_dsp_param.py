import time
import json
import ltamp
from ltamp.protocol import _msg
from ltamp.protocol.SetDspUnitParameter_pb2 import SetDspUnitParameter

amp = ltamp.LtAmp(debug=True)
amp.connect()

amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

cp = amp.request_current_preset()
print("Current preset slot:", cp.get("index"))
pdata = json.loads(cp.get("data", "{}"))
nodes = pdata.get("audioGraph", {}).get("nodes", [])
for n in nodes:
    print("Node:", n.get("nodeId"), "FenderId:", n.get("FenderId"), "params:", n.get("dspUnitParameters"))

print("\n--- TEST: Toggle 'stomp' bypass to True ---")
try:
    amp.send_sync_begin()
    msg = _msg(setDspUnitParameter=SetDspUnitParameter(nodeId="stomp", parameterId="bypass", boolParameter=True))
    amp.send_message(msg)
    amp.send_sync_end()
    print("Sent stomp bypass=True")
except Exception as e:
    print("Failed to send stomp bypass:", e)

time.sleep(1.0)

print("\n--- TEST: Toggle 'stomp' bypass to False ---")
try:
    amp.send_sync_begin()
    msg = _msg(setDspUnitParameter=SetDspUnitParameter(nodeId="stomp", parameterId="bypass", boolParameter=False))
    amp.send_message(msg)
    amp.send_sync_end()
    print("Sent stomp bypass=False")
except Exception as e:
    print("Failed to send stomp bypass:", e)

time.sleep(1.0)
amp.disconnect()
print("Done.")
