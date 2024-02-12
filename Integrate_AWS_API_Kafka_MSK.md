## Integrating AWS API Gateway with Kafka on MSK
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
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler 
```

4. Deploy API
Make note of the Invoke URL after deploying the API. The Kafka REST Proxy URL will look like:

'https://YourAPIInvokeURL/test/topics/'<AllYourTopics>

5. Start the REST Proxy
Navigate to confluent-7.2.0/bin and run:
```bash
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```