#We will need to import the following libraries first:
# pyspark functions
from pyspark.sql.functions import *
# URL processing
import urllib

#Now let's read the table containing the AWS keys to Databricks using the code below:
# Define the path to the Delta table
delta_table_path = "dbfs:/user/hive/warehouse/authentication_credentials"

# Read the Delta table to a Spark DataFrame
aws_keys_df = spark.read.format("delta").load(delta_table_path)
# Get the AWS access key and secret key from the spark dataframe
ACCESS_KEY = aws_keys_df.select('Access key ID').collect()[0]['Access key ID']
SECRET_KEY = aws_keys_df.select('Secret access key').collect()[0]['Secret access key']
# Encode the secrete key
ENCODED_SECRET_KEY = urllib.parse.quote(string=SECRET_KEY, safe="")
# AWS S3 bucket name
AWS_S3_BUCKET = "bucket-name" #user-0a0c9995b889-bucket is just an example pleas replace with your own bucket name 
# Mount name for the bucket
MOUNT_NAME = "/mnt/mount_name" #/mnt/biruk_buket replace  with you mount name 
# Source url
SOURCE_URL = "s3n://{0}:{1}@{2}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_S3_BUCKET)
# Mount the drive
dbutils.fs.mount(SOURCE_URL, MOUNT_NAME)
