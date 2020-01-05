from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime

# Choose the appropriate client
client = MongoClient()

# Connect to the db
db = client.paulisasnake

# Use the collection
coll = db.humid_storage

vals = coll.find({
	"time": {
		'$gte': ISODate("2019-12-11T00:00:00.000Z"),
		'$lt': ISODate("2019-12-14T00:00:00.000Z")
	}
})

print(vals)