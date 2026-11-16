import ltamp
amp = ltamp.LtAmp()
amp.connect()
amp.send_sync_begin()
amp.send_sync_end()
cp = amp.request_current_preset()
print("Amp current slot:", cp.get("index"))
amp.disconnect()
