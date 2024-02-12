# pyspark functions
from pyspark.sql.functions import *
# URL processing
import urllib
# list of topic names in the AWS S3 buket 
topic_names=['0a0c9995b889.geo','0a0c9995b889.pin','0a0c9995b889.user'] # replace with your topic names in your AWS S3 buket
#loop through thr list and read each table one by one 
for i in topic_names:
  file_location = f"/buket-name/topics/{i}/partition=0/"
  file_type = "json"

# Ask Spark to infer the schema
  infer_schema = "true"
  if 'geo'in i :
     # Read in JSONs from the mounted S3 bucket
    df_geo = spark.read.format(file_type) \
    .option("inferSchema", infer_schema) \
    .load(file_location)

   # Display Spark dataframe to check its content
    display(df_geo)
  elif 'pin' in i:
    df_pin = spark.read.format(file_type) \
    .option("inferSchema", infer_schema) \
    .load(file_location)

   # Display Spark dataframe to check its content
    display(df_pin)

  else:
    df_user = spark.read.format(file_type) \
    .option("inferSchema", infer_schema) \
    .load(file_location)

   # Display Spark dataframe to check its content
    display(df_user)