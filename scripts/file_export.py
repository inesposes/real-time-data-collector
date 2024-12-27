import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os 

load_dotenv()

server = os.getenv('SERVER')
mongo_client_uri='mongodb://'+server+':27017/'
client = MongoClient(mongo_client_uri)
client = MongoClient('mongodb://10.133.27.157:27017/')
db = client['bicicorunha']
collection =db['stations']

pipeline = [
    {
        "$project": {
            "_id": 0,
            "id": 1, 
            "name": 1,
            "timestamp": 1,
            "free_bikes": 1,
            "empty_slots": 1,
            "uid": 1,
            "last_updated": 1,
            "slots": 1,
            "normal_bikes": 1,
            "ebikes": 1
        }
    }
]

stations = collection.aggregate(pipeline)
df_stations=pd.DataFrame(list(stations))
client.close()

df_stations.to_parquet('datasets/stations.parquet')
df_stations.to_csv('datasets/stations.csv')
print('CSV and Parquet files created succesfully')