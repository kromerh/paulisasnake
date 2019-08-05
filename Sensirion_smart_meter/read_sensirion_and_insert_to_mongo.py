from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime
import binascii
import struct
import pygatt.backends
from time import sleep

# READ SENSIRION SMART METER
MACADDR='EF:F9:AA:8B:FC:94'
TEMP_NOTI_UUID = '00002235-b38d-4985-720e-0f993a68ee41'
HUMI_NOTI_UUID = '00001235-b38d-4985-720e-0f993a68ee41'
ADDRTYPE = pygatt.backends.BLEAddressType.random


adapter = pygatt.backends.GATTToolBackend()
adapter.start()
connected = False
attempts = 5


device = adapter.connect(MACADDR,10,ADDRTYPE)

# device = adapter.connect(MACADDR)
# print("connected")

temp = device.char_read(TEMP_NOTI_UUID)
tempf = struct.unpack('<f',temp)
print(f'read temp {tempf}')


humi = device.char_read(HUMI_NOTI_UUID)
humif = struct.unpack('<f',humi)
print(f'read humi {humif}')


device.disconnect()
adapter.stop()

# save in the MongoDB
# Choose the appropriate client
client = MongoClient()

# Connect to the test paulisasnake
db = client.paulisasnake

# Use the employee collection
coll_test = db.temp_and_humid

# ====== Inserting Documents ====== #
# Creating a simple Pandas DataFrame
time = pd.Timestamp.now()
data = {
	'time': time,
	'temp': tempf,
	'humid': humif
       }

df = pd.DataFrame(data)
# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
coll_test.insert_many(df.to_dict('records'))


