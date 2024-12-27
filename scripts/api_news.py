import time
import requests
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os 

load_dotenv()

server = os.getenv('SERVER')
mongo_client_uri='mongodb://'+server+':27017/'
client = MongoClient(mongo_client_uri)
db = client['news']
collection =db['technews']
#API Request
api_key = os.getenv("NEWS_API_KEY")
headers = {
    'Authorization': f'Bearer {api_key}'
}
while True: 
    date_now = datetime.now()
    date_yesterday = date_now - timedelta(days=1)
    endpoint='https://newsapi.org/v2/everything?q=tech&from='+date_yesterday.strftime('%Y-%m-%d')+'&to='+date_now.strftime  ('%Y-%m-%d')+'&sortBy=popularity&apiKey=5d286ef61a0b48a2b3c9ff72838cbec9'

    response=requests.get(endpoint, headers=headers)
    response_json=response.json()
    news=response_json['articles']
    try:
        result = collection.insert_many(news)
        print("100 records have been successfully inserted. Now you have to wait one day!")
    except Exception as e:
        print("Error inserting: "+ str(e))
    time.sleep(86400) #Executed every 300sec (5min)

