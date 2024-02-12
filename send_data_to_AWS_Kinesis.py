import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from db_utils import AWSDBConnector


random.seed(100)

def make_payload(data,streaming):
    #payload = json.dumps({
           # "records": [{"value": data}]
            #})
    #for streaming, data in topics_data.items():
    payload = json.dumps({
        "stream-name": streaming,
        "Data": data,
        "PartitionKey": streaming
    })
    return payload



def run_infinite_post_data_loop():

    new_connector = AWSDBConnector()

    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)

            # convert to date and time 
            user_result['date_joined'] = user_result['date_joined'].isoformat()
            #pin_result['timestamp'] = pin_result['timestamp'].isoformat()
            geo_result['timestamp'] = geo_result['timestamp'].isoformat()
            topics_data = {
            'streaming-0a0c9995b889-user': user_result,
            'streaming-0a0c9995b889-pin': pin_result,
            'streaming-0a0c9995b889-geo': geo_result
             }
            headers = {'Content-Type': 'application/json'}
            for streaming, data in topics_data.items():
               api_url =  "https://8f6j2qmbgi.execute-api.us-east-1.amazonaws.com/for_Kinesis/streams/"+ streaming + "/record" 
               payload=make_payload(data,streaming)
               response = requests.put(api_url, headers=headers, data=payload)
               

            if response.status_code== 200:
                print(f"Data sent to kinesis successfully.response status: {response.status_code}")
                print(response.json())
            else:
                print(f"Failed to send data to kinesis. Status code: {response.status_code}")
            
  
if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')