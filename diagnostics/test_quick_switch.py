import time
import ltamp

t0 = time.time()
print(f"Connecting and setting slot 4...")
amp = ltamp.LtAmp()
amp.connect()
t1 = time.time()
amp.send_sync_begin()
amp.set_preset(4)
amp.send_sync_end()
t2 = time.time()
amp.disconnect()
t3 = time.time()

print(f"Total time: {(t3 - t0)*1000:.1f}ms (Connect: {(t1-t0)*1000:.1f}ms, Send: {(t2-t1)*1000:.1f}ms, Close: {(t3-t2)*1000:.1f}ms)")
