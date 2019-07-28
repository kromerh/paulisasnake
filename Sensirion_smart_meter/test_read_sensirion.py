import binascii
import struct
import pygatt.backends


MACADDR='EF:F9:AA:8B:FC:94'
TEMP_NOTI_UUID = '00002235-b38d-4985-720e-0f993a68ee41'
HUMI_NOTI_UUID = '00001235-b38d-4985-720e-0f993a68ee41'

adapter = pygatt.backends.GATTToolBackend()
adapter.start()

# device = adapter.connect(MACADDR,5,'random')
device = adapter.connect(MACADDR)
print("connected")

temp = device.char_read(TEMP_NOTI_UUID)
tempf = struct.unpack('<f',temp)
print("read temp : %.2f" % tempf)


humi = device.char_read(HUMI_NOTI_UUID)
humif = struct.unpack('<f',humi)
print("read humi : %.2f" % humif)



device.disconnect()
adapter.stop()