import pandas as pd
from pymongo import MongoClient


# Choose the appropriate client
client = MongoClient()

# Connect to the db paulisasnake
db = client.paulisasnake

# Use the collection temp and humid
coll = db.temp_and_humid

# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
# coll.insert_many(data.to_dict('records'))


# ====== Finding Documents ====== #
documents = coll.find().sort({x:1}).limit(60)
data = pd.DataFrame(list(documents))
print(data)
