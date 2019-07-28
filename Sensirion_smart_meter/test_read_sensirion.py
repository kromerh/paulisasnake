import binascii
import struct
import pygatt.backends


MACADDR='EF:F9:AA:8B:FC:94'
TEMP_NOTI_UUID = '00002235-b38d-4985-720e-0f993a68ee41'
HUMI_NOTI_UUID = '00001235-b38d-4985-720e-0f993a68ee41'
ADDRTYPE = pygatt.backends.BLEAddressType.random

adapter = pygatt.backends.GATTToolBackend()
adapter.start()

device = adapter.connect(MACADDR,5,ADDRTYPE)
# device = adapter.connect(MACADDR)
print("connected")

temp = device.char_read(TEMP_NOTI_UUID)
tempf = struct.unpack('<f',temp)
print(f'read temp {tempf}')


humi = device.char_read(HUMI_NOTI_UUID)
humif = struct.unpack('<f',humi)
print(f'read humi {humif}')



device.disconnect()
adapter.stop()