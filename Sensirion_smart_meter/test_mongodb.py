from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime

# Choose the appropriate client
client = MongoClient()

# Connect to the test db
db = client.test

# Use the employee collection
coll_test = db.testcollection

# ====== Inserting Documents ====== #
# Creating a simple Pandas DataFrame
time = pd.Timestamp.now()
data = {'time': time,
       'in': np.random.random(1)*1000}
df = pd.DataFrame(data)
# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
coll_test.insert_many(df.to_dict('records'))