from user_posting_emulation import  run_infinite_post_data_loop
import requests
import json

   # Example data for three tables
user_result, pin_result, geo_result = run_infinite_post_data_loop()
topic_1= [ user_result]
topic_2= [ pin_result]
topic_3= [ geo_result]

            # Modify with your API endpoint URL
api_base_url = "https://8f6j2qmbgi.execute-api.us-east-1.amazonaws.com/pintrest_pro/test/topics/"

            # Function to send data to API endpoint for multiple topics
def send_data_to_api(topics_data):
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}

    for topic, data in topics_data.items():
        api_url = api_base_url + topic
        payload = json.dumps({
        "records": [{"value": record} for record in data]
        })

        response = requests.post(api_url, headers=headers, data=payload)
        if response.status_code == 200:
             print(f"Data sent to {topic} successfully.")
        else:
             print(f"Failed to send data to {topic}. Status code: {response.status_code}")

# Prepare a dictionary mapping topics to their respective data
topics_data = {
    '0a0c9995b889.user': topic_1,
    '0a0c9995b889.pin': topic_2,
    '0a0c9995b889.geo': topic_3
}

# Send data from multiple tables to their respective Kafka topics via the API endpoint
send_data_to_api(topics_data)


#invoke_url = "https://8f6j2qmbgi.execute-api.us-east-1.amazonaws.com/pintrest_pro"

