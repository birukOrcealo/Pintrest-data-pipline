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


def make_payload(data): # Function to create payload
    # Create JSON object with data
    payload = json.dumps({  # json.dumps converts Python object to JSON string
        "records": [{"value": data}]  # Wrap data in a list of records
    })
    return payload # Return the payload

def run_infinite_post_data_loop():
# Create a new instance of the AWSDBConnector class
    new_connector = AWSDBConnector()
   

# Run an infinite loop to continuously post data
    while True:
        #Introduce random delay between posts
        sleep(random.randrange(0, 2))
        
        # Generate a random row number within the data
        random_row = random.randint(0, 11000)
        
        # Create a database engine using the AWSDBConnector
        engine = new_connector.create_db_connector()
        
        # Connect to the database
        with engine.connect() as connection:
            
            # Select a random row from the pin_data table
            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            #  Extract the selected row into a dictionary
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
            # Select a random row from the geolocation_data table
            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            # Extract the selected row into a dictionary
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
            # Select a random row from the user_data table
            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            # Extract the selected row into a dictionary
            for row in user_selected_row:
                user_result = dict(row._mapping)

            # Convert date and time values to ISO format
            user_result['date_joined'] = user_result['date_joined'].isoformat()
            geo_result['timestamp'] = geo_result['timestamp'].isoformat()
            
            #  Prepare the data to be posted to the API
            topics_data = {
            '0a0c9995b889.user': user_result,
            '0a0c9995b889.pin': pin_result,
            '0a0c9995b889.geo': geo_result
             }
            
            #Set the headers for the API request
            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            
            # Iterate through topics and post data to each topic
            for topic, data in topics_data.items():
               # Construct the API URL for the current topic
               api_url =  "https://8f6j2qmbgi.execute-api.us-east-1.amazonaws.com/pintrest_pro_new/topics/" + topic
               
               # Create the payload for the API request
               payload=make_payload(data)

               # Send a POST request to the API
               response = requests.post(api_url, headers=headers, data=payload)
               
            # Check the response status code
            if response.status_code == 200:
                print(f"Data sent to pin successfully.")
            else:
                print(f"Failed to send data to pin. Status code: {response.status_code}")
            
  
    
# Execute the run_infinite_post_data_loop function if this script is run as the main module
if __name__ == "__main__":
    run_infinite_post_data_loop()
    # Print a message indicating that the script is still working after the loop exits
    print('Working')