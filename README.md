![Screenshot 2024-02-12 224952](https://github.com/birukOrcealo/Pintrest-data-pipline/assets/118835094/3035fed5-39d9-4ab6-a769-38c61d4994f5)
## table of contents
- [Overview](#overview)

- [Launching EC2 Instance](#launching-ec2-instance)
- [Security Considerations](#security-considerations)
- [Connecting to EC2 Instances](#connecting-to-ec2-instances)
- [Setting Up Kafka on EC2 Instance](#Setting-Up-Kafka-on-EC2-Instance)
- [Install Kafka on Client Machine](#Install-Kafka-on-Client-Machine)
- [ Configure Kafka Client to Use AWS IAM](#Configure-Kafka-Client-to-Use-AWS-IAM)
- [Create a Topic on a Client Machine](#create-a-topic-on-client-machine)
- [MSK Connect and S3 Integration](#MSK-Connect-and-S3-Integration)

- [Integrating AWS API Gateway with Kafka on MSK](#Integrating-AWS-API-Gateway-with-Kafka-on-MSK)
- [Send Data to the API](#Send-Data-to-the-API)
- [Mount AWS S3 Bucket to Databricks](#mount-aws-s3-bucket-to-databricks)
- [Orchestrating Databricks workloads on AWS MWAA](#orchestrating-databricks-workloads-on-aws-mwaa)

- [create data streams using Kinesis Data Streams](#data-streams-using-kinesis-data-streams)
- [API Repsonses in Python](#api-responses-in-python)

## overview
- Pinterest, a platform known for crunching billions of data points daily to enhance user experience, serves as the inspiration for this project. By harnessing the power of the AWS Cloud, this initiative aims to develop a comparable data processing system capable of delivering actionable insights and value to users.


## Launching EC2 Instance
#### Step 1: Access the EC2 Home Page

Log into your AWS account and navigate to the EC2 service from the Management Console.

#### Step 2: Launching an Instance

Click on the Launch Instance button in the EC2 Dashboard.

#### Step 3: Selecting an AMI

Choose an AMI (Amazon Machine Image) for your instance.

#### Step 4: Selecting an Instance Type

Select the desired instance type, e.g., t3.micro.

#### Step 5: Configuring the Networking Settings

Configure networking settings, such as VPC, subnet, and security groups.
## Security Considerations
#### SSH Protocol

SSH is a secure protocol for remote access. The default security group allows SSH access from any source IP address (0.0.0.0/0). Consider restricting access to trusted IP addresses.

#### Source IP Address

The default rule permits SSH access from any source IP address. For increased security, restrict SSH access to specific trusted IPs, like your organization's range or your home IP.

## Connecting to EC2 Instances


### Step 1: Create a Key Pair Locally

1. Navigate to Parameter Store in your AWS account.
2. Using your KeyPairId, find the specific key pair associated with the EC2 instance.
3. Select this key pair, and under the Value field, select Show. Copy the entire value (including BEGIN and END header) and paste it into a new file with the .pem extension in VSCode.

### Step 2: Save Key Pair

1. Navigate to the EC2 console.
2. Select the EC2 instance, and under the Details section, find the Key pair name.
3. Save the previously created file in VSCode using the following format: Key pair name.pem.

### Step 3: Connect to EC2 Instance

Now you are ready to connect to your EC2 instance.

1. Open an SSH client.
2. Locate your private key file (e.g., 0a0c9995b889-key-pair.pem).
3. Run the following command to ensure your key is not publicly viewable. pleas replace 0a0c9995b889-key-pair.pem with your private key file name 
```bash 
chmod 400 "0a0c9995b889-key-pair.pem" 
```
4. Connect to your instance using its Public DNS:ec2-54-173-183-37.compute-1.amazonaws.com for example 

```bash 
ssh -i "0a0c9995b889-key-pair.pem" root@ec2-54-173-183-37.compute-1.amazonaws.com   
# replace 0a0c9995b889-key-pair.pem  with actuall file name 
```
  
 

##  Setting Up Kafka on EC2 Instance


### Create a Cluster

To create an Amazon MSK cluster using the Management Console, follow these steps:

1. Sign in to the Management Console and open the Amazon MSK console.
2. Choose "Create Cluster."
3. Choose between "Quick create" and "Custom create" options. Customize settings like security, availability, and configuration with the "Custom create" option.
4. Provision broker instances and broker storage. Broker instances are worker nodes managing the Kafka cluster, and broker storage stores incoming data.
5. The status changes from "Creating" to "Active" once AWS provisions the cluster.

### View Client Information

1. Select the desired cluster from the Clusters list in the MSK Console.
2. Choose "View client information" to access cluster details.
3. Find the Bootstrap servers' information under the "Private endpoint" section. Note the bootstrap brokers string.
4. Obtain the Apache Zookeeper connection string with host:port pairs for plaintext and TLS communication.

### Allow Client Machine to Send Data

Ensure the client machine can send data to the MSK cluster:

1. Check the Security groups of the cluster's Virtual Private Cloud (VPC).
2. Open the VPC console and under Security, select Security groups.
3. Edit inbound rules, add a rule with "All traffic" type, and set the source as the client machine's security group ID.

## Install Kafka on Client Machine

1. Connect to the EC2 client machine and install Java:

```bash
sudo yum install java-1.8.0
```
2. Download and extract Apache Kafka:

```bash
wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
tar -xzf kafka_2.12-2.8.1.tgz
```



#### For MSK clusters with IAM authentication:

1. Navigate to the Kafka installation folder and then the "libs" folder.
2. Download the IAM MSK authentication package from GitHub:

```bash 
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar
```

#### CLASSPATH Environment Variable

1. After downloading the aws-msk-iam-auth-1.1.5-all.jar file, create an environment variable called CLASSPATH to store the location of this jar file. The CLASSPATH ensures that the Amazon MSK IAM libraries are accessible to the Kafka client, regardless of the working directory.

```bash 
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```
2. To persist the CLASSPATH environment variable across sessions, add the export command to the .bashrc file:

```bash 
echo 'export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar' >> ~/.bashrc
source ~/.bashrc
```

## Configure Kafka Client to Use AWS IAM

To configure a Kafka client to use AWS IAM for authentication, follow these steps:

1. Navigate to your Kafka installation folder and then to the `bin` folder.
2. Create a `client.properties` file using the following command:

```bash
nano client.properties
```

3. Add the following configurations to the client.properties file:

``` bash
# Sets up TLS for encryption and SASL for authN.
security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="Your Access Role";

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler

```
## Create a Topic on a Client Machine
- To create a topic, ensure you are inside your <KAFKA_FOLDER>/bin and then run the following command, replacing BootstrapServerString with the connection string you have previously saved and <topic_name> with your desired topic name:

```bash
./kafka-topics.sh --bootstrap-server BootstrapServerString --command-config client.properties --create --topic <topic_name>
```

## MSK Connect and S3 Integration

### Step 1: Create S3 Bucket

Create an S3 bucket in your AWS account to store the data exported from Kafka topics.

### Step 2: Create IAM Role

1. Navigate to the IAM console.
2. Select Roles under the Access management section.
3. Choose Create role to create a new IAM role.
4. Under Trusted entity type, select AWS service, and under the Use case field, select S3 in the Use cases for other AWS services field.
5. In the permission tab, select Create policy.Replace the existing text with the following policy:

```json

    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::<DESTINATION_BUCKET>",
                "arn:aws:s3:::<DESTINATION_BUCKET>/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucketMultipartUploads",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        }
    ]
 ```



5. Select the policy and proceed to create the role.
6. In the IAM console, choose the role you have just created.
7. select the Trust relationships tab.
8. In the Trusted entities tab you should add the following trust policy:

```json

    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "kafkaconnect.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]

```

### Step 3: Create VPC Endpoint to S3

1. In the VPC console, select Endpoints under the Virtual private cloud tab.
2. Choose Create endpoint.
3. Under Service Name, choose com.amazonaws.<your-region>.s3 and the Gateway type.
4. Select the VPC corresponding to the MSK cluster's VPC from the drop-down menu in the VPC section.
5. Create the endpoint.

### Step 4: Create Custom Plugin

1. Connect to your client EC2 machine.
2. Download the Confluent.io Amazon S3 Connector and copy it to the S3 bucket.To do download & copy this connector run the code below inside your client machine:
```bash
# assume admin user privileges
sudo -u ec2-user -i
# create directory where we will save our connector 
mkdir kafka-connect-s3 && cd kafka-connect-s3
# download connector from Confluent
wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-s3/versions/10.0.3/confluentinc-kafka-connect-s3-10.0.3.zip
# copy connector to our S3 bucket
aws s3 cp ./confluentinc-kafka-connect-s3-10.0.3.zip s3://<BUCKET_NAME>/kafka-connect-s3/

```
3. Open the MSK console and select Custom plugins under the MSK Connect section.
4. Choose Create custom plugin.
5. Select the bucket and ZIP file for the Confluent connector.
6. Give the plugin a name and create it.

### Step 5: Create Connector

1. In the MSK console, select Connectors under the MSK Connect section.
2. Choose Create connector.
3. Select the custom plugin you created.
4. Provide a name for the connector and select your MSK cluster.
5. Copy the following  connector configuration settings.

``` bash
### configutaion setting
connector.class=io.confluent.connect.s3.S3SinkConnector
# same region as our bucket and cluster
s3.region=us-east-1
flush.size=1
schema.compatibility=NONE
tasks.max=3
# include nomeclature of topic name, given here as an example will read all data from topic names starting with msk.topic....
topics.regex=<YOUR_UUID>.*
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
value.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
storage.class=io.confluent.connect.s3.storage.S3Storage
key.converter=org.apache.kafka.connect.storage.StringConverter
s3.bucket.name=<BUCKET_NAME> 
```


6. Create the connector.

Make sure to replace placeholders like `<DESTINATION_BUCKET>`, `<BUCKET_NAME>`, `<YOUR_UUID>`, and `<your-region>` with your actual values.

## Integrating AWS API Gateway with Kafka on MSK

- This guide walks you through the process of setting up a Kafka REST Proxy integration with AWS API Gateway, allowing you to create a RESTful interface to interact with a Kafka cluster.

### Step 1 : Create API Gateway

1. Go to the [API Gateway console](https://console.aws.amazon.com/apigateway).
2. Create a new API with a `{proxy+}` resource.
3. Set up an integration by clicking on the ANY resource and then the Edit integration button.
   - For HTTP method, select ANY.
   - Use your Kafka Client EC2 Instance Public DNS as the Endpoint URL.
     - Obtain the EC2 Instance Public DNS from the EC2 console.
   - The Endpoint URL format should be: `http://KafkaClientEC2InstancePublicDNS:8082/{proxy}`.

### Step 2 : Install Confluent Package for REST Proxy on EC2 Client

On your EC2 instance, run the following commands:
```bash 
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
tar -xvzf confluent-7.2.0.tar.gz
```
1. Navigate to confluent-7.2.0/etc/kafka-rest and edit kafka-rest.properties:

```bash
nano kafka-rest.properties
```
2. Modify the bootstrap.servers and zookeeper.connect variables with the corresponding Boostrap server string and Plaintext Apache Zookeeper connection string.

3. Add IAM authentication settings to kafka-rest.properties:
``` bash
### kafka-rest.properties
# Zookeeper and Bootstrap strings
zookeeper.connect=<ZookperString>
bootstrap.servers=<BootstrapServerString>

# Sets up TLS for encryption and SASL for authN.
client.security.protocol = SASL_SSL
# Identifies the SASL mechanism to use.
client.sasl.mechanism = AWS_MSK_IAM
# Binds SASL client implementation.
client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="<awsEC2RoleARN>";
# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler ``

4. Deploy API
Make note of the Invoke URL after deploying the API. The Kafka REST Proxy URL will look like:

'https://YourAPIInvokeURL/test/topics/'<AllYourTopics>

5. Start the REST Proxy
Navigate to confluent-7.2.0/bin and run:
```bash
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```

## Send Data to the API
#### Step 1: Modify Script
Modify Send_Data_to_API_Gateway.py file in the repository to send data to your Kafka topics using your API Invoke URL. Send data from the three tables to their corresponding Kafka topic.

#### Step 2: Check Consumed Data
Run a Kafka consumer (one per topic) to check if messages are being consumed.

#### Step 3: Verify S3 Storage
Check if data is getting stored in the S3 bucket. Observe the folder organization (e.g., topics/<your_UserId>.pin/partition=0/) created by your connector in the bucket.

## Mount AWS S3 Bucket to Databricks

The `Mount_S3_databricks.py` file contains all the code necessary to mount Databricks with the S3 bucket and read data from the mounted S3 bucket for data processing.

### step 1: creat AWS Access Key and Secret Access Key for Databricks 

1. Access the IAM console in your AWS account.

2. In the IAM console, under Access management click on Users.

3. Click on the Add users button.

4. Enter the desired User name and click Next.

5. On the permission page, select the Attach existing policies directly choice. In the search bar type AmazonS3FullAccess and check the box. (This will allow full access to S3, meaning Databricks will be able to connect to any existing buckets on the AWS account.)

6. Skip the next sections until you reach the Review page. Here select the Create user button.

7. Now that you have created your IAM User, you will need to assign it a programmatic access key:
 - In the Security Credentials tab select Create Access Key
 - On the subsequent page select Command Line Interface (CLI), navigate to the bottom of the page click I understand
 - On the next page, give the keypair a description and select Create Access Key
8. Click the Download.csv file button to download the credentials you have just created.

### Step 2: Upload credential csv file to Databricks

1. In the Databricks UI, click the Catalog icon and then click + Add --> Add data button.

2. Click on Create or modify table and then drop the credentials file you have just downloaded from AWS. Once the file has been successfully uploaded, click Create table to finalize the process.

### Step 3: Mount S3 bucket to Databricks

1. Select the New icon and then select Notebook.

2. Mount the S3 bucket to Databricks.
  - We will need to import the following libraries first:

``` python
# pyspark functions
from pyspark.sql.functions import *
# URL processing
import urllib  
```
 - read the table containing the AWS keys to Databricks using the code below:

``` python 
# Define the path to the Delta table
delta_table_path = "dbfs:/user/hive/warehouse/authentication_credentials"
# Read the Delta table to a Spark DataFrame
aws_keys_df = spark.read.format("delta").load(delta_table_path)
```
-  extract the access key and secret access key from the spark dataframe created above. 

```python 
Get the AWS access key and secret key from the spark dataframe
ACCESS_KEY = aws_keys_df.select('Access key ID').collect()[0]['Access key ID']
SECRET_KEY = aws_keys_df.select('Secret access key').collect()[0]['Secret access key']
# Encode the secrete key
ENCODED_SECRET_KEY = urllib.parse.quote(string=SECRET_KEY, safe="")
```
- We can now mount the S3 bucket by passing in the S3 URL and the desired mount name to dbutils.fs.mount(). Make sure to replace the AWS_S3_BUCKET with the name of the bucket you have your data stored into, and MOUNT_NAME with the desired name inside your Databricks workspace.

``` python 
# AWS S3 bucket name
AWS_S3_BUCKET = "bucket_name"
# Mount name for the bucket
MOUNT_NAME = "/mnt/mount_name"
# Source url
SOURCE_URL = "s3n://{0}:{1}@{2}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_S3_BUCKET)
# Mount the drive
dbutils.fs.mount(SOURCE_URL, MOUNT_NAME)
```

### Step 4: Read data from the mounted S3 bucket

1. To check if the S3 bucket was mounted succesfully run the following command:

```python 
display(dbutils.fs.ls("/mnt/mount_name/../.."))
```

2. Read the JSON format dataset from S3 into Databricks using the code cells below:

```python
# File location and type
# Asterisk(*) indicates reading all the content of the specified file that have .json extension
file_location = "/mnt/mount_name/filepath_to_data_objects/*.json" 
file_type = "json"
# Ask Spark to infer the schema
infer_schema = "true"
# Read in JSONs from mounted S3 bucket
df = spark.read.format(file_type) \
.option("inferSchema", infer_schema) \
.load(file_location)
# Display Spark dataframe to check its content
display(df)
```
### Step 5 (Optional): Unmount S3 bucket
 - If you want to unmount the S3 bucket, run the following code:
 ```python
 dbutils.fs.unmount("/mnt/mount_name")
 ```

## Orchestrating Databricks workloads on AWS MWAA

#### step 1 : Create an API token in Databricks
#### step 2 : Create the MWAA to Databricks connection
#### step 3 : Create the Airflow DAG
 - in the repositary you have a example of DAG.py file that will run a Databricks Notebook on a specific schedule. Once you have created your DAG, you should upload it to the MWAA S3 bucket in the dags folder.
 

 ## create data streams using Kinesis Data Streams

-  Navigate to the Kinesis console, and select the Data Streams section. Choose the Create stream button.

- Choose the desired name for your stream and input this in the Data stream name field. For our use case we will use the On-demand capacity mode.

- Once you have entered the name and chose the capacity mode click on Create data stream. When your stream is finished creating the Status will change from Creating to Active.

## Integrating AWS API Gateway with AWS Kinesis
 
 #### step 1 : Create an IAM role for API access to Kinesis.To enable full access to Kinesis, you can create an IAM role in the IAM console that assumes the **AmazonKinesisFullAccessRole** policy. This will enable both read-write actions in Kinesis.

 #### step 2 : List streams in Kinesis:To begin building our integration navigate to the Resources tab of the previously created API. Use the Create resource button to start provisioning a new resource:Under Resource Name, type streams. Leave the rest as default and then click the Create resource button.

 #### step 3 : Choose the created streams resource, and then select the Create method button. Select GET as the method type.In the Create method page you will need to define the following:

      -  For Integration type select AWS Service
      -  For AWS Region choose region of your choice 
      -  For AWS Service select Kinesis,
      -  For HTTP method select POST (as we will have to invoke Kinesis's ListStreams action)
      -  For Action Type select User action name
      - For Action name type ListStreams
      - For Execution role you should copy the ARN of your Kinesis Access Role (created in the previous section)
      - Finally, click Create method to finalize provisioning this method.
#### step.4 configure the **integration request**: 
      - select **integration request**  panal,click on the EDIT button 
      - Expand the URL request headers  parameters panel and select the following options:
      - Under Name type Content-Type
      - Under Mapped form type 'application/x-amz-json-1.1'
      - Click the Add request header parameter button
      - Expand the Mapping Templates panel and select the following options:
      - Choose Add mapping template button
      - Under Content-Type type application/json
      - Under Template body type {} in the template editor
#### step.5 Create, **describe and delete streams** in Kinesis
      - Under the streams resource create a new child resource with the Resource name {stream-name}.
      - Create the following three Methods for {stream-name} resource: POST, GET and DELETE.
#### step.6 settting up the GET methods 
- For Integration type select AWS Service
- For AWS Region choose region
- For AWS Service select Kinesis
- For HTTP method select POST
-  For Action select User action name
- For Action name type DescribeStream
- For Execution role you should use the same ARN as in the previous step
- Finally, click Create method.  This will redirect you to the Method Execution page
- select the Integration Request panel, and then Edit. Expand the URL request headers parameters panel and select the following options:
- Click on the Add request header parameter button
- Under Name type Content-Type
- Under Mapped form type 'application/x-amz-json-1.1'
- Expand the Mapping Ttemplates - panel and select the following options:
- Click on the Add mapping - template button
- Under Cotent-Type type application/json
- In the Template body include the following:
        
        ```
        "StreamName": "$input.params('stream-name')"
        ```
- setting up thr POST method
- follow **step.6** but in the Action name section type CreateStream
For setting up the URL request headers parameters section follow step.6.
- For setting up the Mapping  Templates panel follow step.6 instruction, but add the following mapping template in the template body instead:
         
         ```
         "ShardCount": #if($input.path('$.ShardCount') == '') 5 #else $input.path ('$.ShardCount') #end,
         "StreamName": "$input.params('stream-name')"
         ```
#### step 7 : setting up the DELET method 
-  follow **step.6** but in the Action name section type DeleteStream
-  For setting up the URL request headers parameters section follow step.6.
 -  For setting up the Mapping  Templates panel follow step.6 instruction, but add the following mapping template in the   template body instead: 

    ```json 
    "StreamName": "$input.params('stream-name')"
    ```
#### step 8 : Add records to streams in Kinesis

- Under the {stream-name} resource create a two new child resources with the Resource Name, record and records. For both resources create a PUT method.
- set up the PUT method for     **record**  resource 
- follow **step.6** but in the Action name section type **PutRecord**
-  For setting up the URL request headers parameters section follow step.6.
 -  For setting up the Mapping  Templates panel follow step.6 instruction, but add the following mapping template in the   template body instead: 
    ```json 
    
    "StreamName": "$input.params('stream-name')",
    "Data": "$util.base64Encode($input.json('$.Data'))",
    "PartitionKey": "$input.path('$.PartitionKey')"

    ```
- set up the PUT method for     **records**  resource 
- follow **step.6** but in the Action name section type **PutRecords**
-  For setting up the URL request headers parameters section follow step.6.
-  For setting up the Mapping  Templates panel follow step.6 instruction, but add the following mapping template in the   template body instead: 

    ```json 
     "StreamName": "$input.params('stream-name')",
    "Records": [
       #foreach($elem in $input.path('$.records'))
          {
            "Data": "$util.base64Encode($elem.data)",
            "PartitionKey": "$elem.partition-key"
          }#if($foreach.hasNext),#end
        #end
    ]
    
    ```
## API Repsonses in Python

  - Now that we have updated our API, we can use the Python requests library to test the new API methods and obtain a response.

 - Make sure to deploy the newest version of your API and use the correct API Invoke URL.

 - **see Send_data_to_AWS_Kinesis.py** file , it shows my actual implimentation in this project
 ```python 
 import requests
import json

example_df = {"index": 1, "name": "Maya", "age": 25, "role": "engineer"}

# invoke url for one record, if you want to put more records replace record with records
invoke_url = "https://YourAPIInvokeURL/<YourDeploymentStage>/streams/<stream_name>/record"

#To send JSON messages you need to follow this structure
payload = json.dumps({
    "StreamName": "YourStreamName",
    "Data": {
            #Data should be send as pairs of column_name:value, with different columns separated by commas      
            "index": example_df["index"], "name": example_df["name"], "age": example_df["age"], "role": example_df["role"]
            },
            "PartitionKey": "desired-name"
            })

headers = {'Content-Type': 'application/json'}

response = requests.request("PUT", invoke_url, headers=headers, data=payload)
 ```
  
