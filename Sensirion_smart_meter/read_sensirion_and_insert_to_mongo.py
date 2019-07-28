from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime
import binascii
import struct
import pygatt.backends
import time

# READ SENSIRION SMART METER
MACADDR='EF:F9:AA:8B:FC:94'
TEMP_NOTI_UUID = '00002235-b38d-4985-720e-0f993a68ee41'
HUMI_NOTI_UUID = '00001235-b38d-4985-720e-0f993a68ee41'
ADDRTYPE = pygatt.backends.BLEAddressType.random

while True:
	adapter = pygatt.backends.GATTToolBackend()
	adapter.start()
	connected = False
	attempts = 5

	for i in range(attempts):
		if connected == False:
			try:
				device = adapter.connect(MACADDR,10,ADDRTYPE)
				connected = True
				print(f'connected: {connected}, attempt: {i}')
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

				# Connect to the test db
				db = client.sensirion_test

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
			except:
				connected = False
				print('Not connected, trying again')
	time.sleep(100)
