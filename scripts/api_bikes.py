import time
import requests
from pymongo import MongoClient
import os


mongo_client_uri = os.getenv('MONGO_URI')  
client = MongoClient(mongo_client_uri)
db = client['bicicorunha']
collection =db['stations']
while True: 
    #API Request
    try:
        endpoint="http://api.citybik.es/v2/networks/bicicorunha"
        response=requests.get(endpoint)
        response_json=response.json()
        stations=response_json['network']['stations']
        try:
            result = collection.insert_many(stations)
        except Exception as e:
            print("Error inserting: "+ str(e))

    except Exception as e:
        print("Error querying the API: "+ str(e))
    time.sleep(300) #Executed every 300sec (5min)
