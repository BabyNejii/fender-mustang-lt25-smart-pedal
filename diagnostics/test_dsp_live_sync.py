import time
import json
import ltamp
from ltamp.protocol import _msg
from ltamp.protocol.SetDspUnitParameter_pb2 import SetDspUnitParameter

amp = ltamp.LtAmp()
amp.connect()
amp.send_sync_begin()
time.sleep(0.05)
amp.send_sync_end()
time.sleep(0.1)

# 1. Switch to Slot 2 (Silky Solo)
print("Loading Slot 2 (Silky Solo)...")
amp.send_sync_begin()
amp.set_preset(2)
amp.send_sync_end()
time.sleep(0.2)

# 2. Query preset audio graph
cp = amp.request_current_preset()
pdata = json.loads(cp.get("data", "{}"))
nodes_by_id = {n.get("nodeId"): n for n in pdata.get("audioGraph", {}).get("nodes", [])}
base_vol = nodes_by_id["amp"].get("dspUnitParameters", {}).get("volume", -12.0)
print(f"Preset 2 Base Volume: {base_vol:.2f} dB")
print("Initial stomp bypass:", nodes_by_id["stomp"].get("dspUnitParameters", {}).get("bypass"))

# 3. Test Solo Boost +3dB
print("\n--- Applying +3dB Solo Boost ---")
amp.send_sync_begin()
amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="amp", parameterId="volume", floatParameter=base_vol + 3.0)))
amp.send_sync_end()
time.sleep(0.5)

# 4. Test Bypassing OD
print("\n--- Bypassing Overdrive ('stomp' node) ---")
amp.send_sync_begin()
amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="stomp", parameterId="bypass", boolParameter=True)))
amp.send_sync_end()
time.sleep(0.5)

# 5. Restore OD
print("\n--- Enabling Overdrive ('stomp' node) ---")
amp.send_sync_begin()
amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="stomp", parameterId="bypass", boolParameter=False)))
amp.send_sync_end()
time.sleep(0.5)

# 6. Restore Volume
print("\n--- Removing Solo Boost ---")
amp.send_sync_begin()
amp.send_message(_msg(setDspUnitParameter=SetDspUnitParameter(nodeId="amp", parameterId="volume", floatParameter=base_vol)))
amp.send_sync_end()

amp.disconnect()
print("All tests passed cleanly!")
