import pandas as pd
import numpy as np
from pymongo import MongoClient


# save in the MongoDB
# Choose the appropriate client
client = MongoClient()

# Connect to the db paulisasnake
db = client.paulisasnake



# load everything from the live
# read all the data from the mongo db collection
coll = db.temp_and_humid
docs = coll.find()
data = pd.DataFrame(list(docs))

# drop the collection
coll.drop()

# process the data to redice number of entries
# store temperature and humidity separately
data_temp = data[['time', 'utc_time', 'temp']]
data_temp = data_temp[data_temp['temp'] > -100]

data_humid = data[['time', 'utc_time', 'humid']]
data_humid = data_humid[data_humid['humid'] > -100]

data_temp = data_temp.sort_values(by='time')
data_humid = data_humid.sort_values(by='time')

def filter_data(delta, data, col):
    """
    Filters the dataset by keeping only those datapoints that deviate more than delta from the
    previous one.
    Returns a pandas dataframe
    """
    data_return = pd.DataFrame()
    data_return['time'] = data['time'].copy()
    data_return['utc_time'] = data['utc_time'].copy()

    # copy temp or humid
    data_return[col] = data[col].copy()

    # shift by 1 and -1
    data_return[f'{col}_p1'] = data_return[col].shift(-1)

    # rolling mean. sampling frequency is around 10 seconds, to take rolling mean of 30 (5 min)
#     data_return[f'{col}_mean'] = data_return[col].rolling(30).mean()

    # create mask if the value is larger than the delta compared to the value before and after
    data_return['diff'] = np.abs(data_return[f'{col}_p1'] - data_return[col])

    data_return['mask'] =  (data_return['diff'] >= delta)
    data_return = data_return[data_return['mask']]

    data_return = data_return[['utc_time','time',col]]
#     print(data_return.head(20))
    return data_return



# store temperature in storage table
data_temp = filter_data(0.05, data_temp, 'temp')
coll = db.temp_storage
# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
coll.insert_many(data_temp.to_dict('records'))



# store humidity in storage table
data_humid = filter_data(0.1, data_humid, 'humid')
coll = db.humid_storage
# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
coll.insert_many(data_humid.to_dict('records'))



