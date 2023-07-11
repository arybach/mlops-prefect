import os
import sys
import pickle
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
from batch import read_data, predict_test_data

def get_input_path(year, month):
    input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def save_to_s3(df, filename, bucket_name='nyc-duration'):
    if os.environ.get("S3_ENDPOINT_URL"):
        if not os.path.exists(filename):
            print(f"File not found: {filename}. Skipping upload.")
            return

        # Initialize the S3 client with the provided credentials
        s3 = boto3.client('s3',
                          endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

        try:
            # Upload the file to S3
            s3.upload_file(filename, bucket_name, filename)
            print(f"Saved file to S3: {filename}")
        except NoCredentialsError:
            print("Unable to access AWS credentials. Please check your credentials.")
    else:
        # Save locally
        df.to_parquet(filename, engine='pyarrow', compression=None, index=False)


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    print('Input file path:', input_file)  # Print the input file path
    print('Output file path:', output_file)  # Print the output file path

    if not os.path.exists("output"):
        os.makedirs("output")

    # Read file from HTTP URL and save it locally as .parquet - this part is needed as S3_ENDPOINT_URL is always no null!
    if not os.path.exists(output_file):
        print('Downloading file from:', input_file)
        df = pd.read_parquet(input_file)
        df.to_parquet(output_file, engine='pyarrow', compression=None)
    
    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(input_file, categorical)
    df_result = predict_test_data(df, year, month)
    print(df_result)
    save_to_s3(df_result, output_file)

if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
    #main(2022, 1)