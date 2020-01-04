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

agg = coll.aggregate([
    {"$group": {
        "_id" : { "$concat": [
            {"$substr": [{"$year": "$time"}, 0, 4 ]},
            "-",
            {"$substr": [{"$month": "$time"}, 0, 2 ]},
            "-",
            {"$substr": [{"$dayOfMonth": "$time"}, 0, 2 ]},
        ]},
        "count": {"$sum": 1 }
     }},
     {"$sort": { "_id": 1 }}
])

dates = [x.to_mongo() for x in agg]

print(dates)