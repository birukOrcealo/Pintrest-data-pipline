### step 1 :creat AWS S3 buket
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

``` json

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

#### step 3 : Create VPC Endpoint to S3

1. In the VPC console, select Endpoints under the Virtual private cloud tab.
2. Choose Create endpoint.
3. Under Service Name, choose com.amazonaws.<your-region>.s3 and the Gateway type.
4. Select the VPC corresponding to the MSK cluster's VPC from the drop-down menu in the VPC section.
5. Create the endpoint.

#### step 4 :Create Custom Plugin

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

