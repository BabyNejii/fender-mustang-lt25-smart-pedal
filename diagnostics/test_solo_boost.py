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
pdata = json.loads(cp.get("data", "{}"))
amp_node = None
for n in pdata.get("audioGraph", {}).get("nodes", []):
    if n.get("nodeId") == "amp":
        amp_node = n
        break

orig_vol = amp_node.get("dspUnitParameters", {}).get("volume", -10.0) if amp_node else -10.0
boosted_vol = orig_vol + 3.0
print(f"Original Volume: {orig_vol:.2f} dB, Boosted Volume (+3dB): {boosted_vol:.2f} dB")

print("\n--- TEST: Apply Solo Boost (+3dB) ---")
amp.send_sync_begin()
msg = _msg(setDspUnitParameter=SetDspUnitParameter(nodeId="amp", parameterId="volume", floatParameter=boosted_vol))
amp.send_message(msg)
amp.send_sync_end()
time.sleep(1.0)

print("\n--- TEST: Remove Solo Boost (Restore Original Volume) ---")
amp.send_sync_begin()
msg = _msg(setDspUnitParameter=SetDspUnitParameter(nodeId="amp", parameterId="volume", floatParameter=orig_vol))
amp.send_message(msg)
amp.send_sync_end()
time.sleep(1.0)

amp.disconnect()
print("Done.")
