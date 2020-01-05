from pymongo import MongoClient
import pandas as pd
import numpy as np
import dateutil
from datetime import datetime, timedelta



# Choose the appropriate client
client = MongoClient()

# Connect to the db
db = client.paulisasnake

# Use the collection
coll = db.humid_storage

start_date_str = "2019-12-11T00:00:00.000Z"
end_date_str = "2019-12-14T00:00:00.000Z"

start_date = dateutil.parser.parse(start_date_str)
end_date = dateutil.parser.parse(end_date_str)

end_date = end_date + timedelta(days=1)

print(end_date)
vals = coll.find({
	"time": {
		'$gte': start_date,
		'$lt': end_date
	}
})

for val in vals:
	print(val)