#### Install Kafka on Client Machine

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
#### Configure Kafka Client to Use AWS IAM

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