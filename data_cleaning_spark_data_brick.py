
# Import required functions from pyspark.sql.functions
from pyspark.sql.functions import col,regexp_extract,regexp_replace
from pyspark.sql.functions import col, concat, lit
#clean the df_pin DataFrame 

#Perform the necessary transformations on the follower_count to ensure every entry is a number.
df_pin = df_pin.withColumn('follower_count', regexp_replace(col('follower_count'), 'k', '000'))
df_pin = df_pin.withColumn('follower_count', regexp_replace(col('follower_count'), 'M', '000000'))
# Make sure the data type of follower_count is an int
df_pin = df_pin.withColumn('follower_count', df_pin['follower_count'].cast('int'))
#Replace empty entries and entries with no relevant data in each column with Nones
df_pin= df_pin.na.fill("None")

# ensure all columns that contain numeric data have numeric data type 
for column in df_pin.columns:
     if 'int' in str(df_pin.schema[column].dataType) or 'double' in str(df_pin.schema[column].dataType):
          df_pin.withcolumn(column,col(column).cast('double'))
#print schema To check whether the operations were successful
df_pin.printSchema()
#Rename the index column to "ind"
df_pin=df_pin.withColumnRenamed('index','ind')

#reorder the columns 
df_pin=df_pin.select('ind','unique_id','title','description','follower_count','poster_name','tag_list','is_image_or_video','image_src','save_location','category')


#clean geo data frame 
#Create a new column coordinates that contains an array based on the latitude and longitude columns
df_geo=df_geo.withColumn('coordinates',array('latitude','longitude'))
#Drop the latitude and longitude columns from the DataFrame
df_geo=df_geo.drop('latitude','longitude')
#Convert the timestamp column from a string to a timestamp data type
df_geo=df_geo.withColumn('timestamp',col('timestamp').cast('timestamp'))
#Reorder the DataFrame columns 
df_geo=df_geo.select('ind','country','coordinates','timestamp')


#cleaning user data frame 

#Create a new column user_name that concatenates the information found in the first_name and last_name columns
df_user=df_user.withColumn('user_name',concat(col('first_name'),lit(" "),col('last_name')))
#Drop the first_name and last_name columns from the DataFrame
df_user=df_user.drop('first_name','last_name')
#Convert the date_joined column from a string to a timestamp data type
df_user=df_user.withColumn('date_joined',col('date_joined').cast('timestamp'))
#Reorder the DataFrame columns
df_user=df_user.select('ind','user_name','age','date_joined')
