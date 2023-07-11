import os
import pandas as pd
from batch import read_data, test_prepare_data, predict_test_data
from test_batch import get_input_path, get_output_path, save_to_s3
import boto3, botocore

def get_file_size(bucket, key):
    if os.environ.get("S3_ENDPOINT_URL"):
        s3 = boto3.client(
            's3',
            endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

        try:
            response = s3.head_object(Bucket=bucket, Key=key)
            return int(response['ContentLength'])
        except botocore.exceptions.ClientError as e:
            print(f"Error getting file size from S3: {bucket}/{key}")
            print(e)
            return 0
    else:
        return 0
    
def read_from_s3(filename):
    if os.environ.get("S3_ENDPOINT_URL"):
        s3 = boto3.client(
            's3',
            endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

        try:
            # Read the file from localstack S3
            s3.download_file('nyc-duration', filename, filename)
            return pd.read_parquet(filename, engine='pyarrow')
        except botocore.exceptions.ClientError as e:
            print(f"Error reading file from S3: {filename}")
            print(e)
            return None
    else:
        return pd.read_parquet(filename)


year = 2022  # Specify the year
month = 1  # Specify the month

input_file = get_input_path(year, month)
output_file = get_output_path(year, month)

# 4 rows created manually
df_test = test_prepare_data()

# Save DataFrame to localstack
file_key = 'output/test_df.parquet'
save_to_s3(df_test, file_key)

# Get the size of the saved file
bucket_name = 'nyc-duration'
file_size = get_file_size(bucket_name, file_key)
print(f"The file size is: {file_size} bytes")

df_result = predict_test_data(df_test, year, month)
print(df_result['predicted_duration'])
print('Sum of predicted durations for test df:', df_result['predicted_duration'].sum())

# Run batch.py script for "January 2022"
os.system(f"python test_batch.py {year} {month}")

# check
categorical = ['PULocationID', 'DOLocationID']
df_run = read_data(input_file, categorical)
df_run = predict_test_data(df_run, year, month)
result_file = f"output/result-{year}-{month:02d}.parquet"
df_run.to_parquet(result_file, engine='pyarrow')
save_to_s3(df_run, result_file)
df_check = read_from_s3(result_file)
print("Predicted durations:", df_check)

#df = pd.read_parquet("output/yellow_tripdata_2022-01.parquet", engine='pyarrow')
#print(df)
