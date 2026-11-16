import ltamp

amp = ltamp.LtAmp()
amp.connect()
pkt = bytearray([0x35, 0x07, 0x08, 0x00, 0x8a, 0x02, 0x02, 0x08, 0x05] + [0]*55)
ret = amp.device.device.write(pkt)
print(f"Device write return: {ret} bytes (expected 64)")
amp.disconnect()
