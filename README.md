Q1. if __name__ == "__main__":
        year = int(sys.argv[1])
    	month = int(sys.argv[2])
	
	main(year, month)
 
[0] % python batch.py 2022 02
predicted mean duration: 12.513422116701408


Q2. Both of the above options are correct

Q3. 4 rows are expected

Q4. --endpoint-url

aws s3 mb s3://nyc-duration --endpoint-url=http://localhost:4566
make_bucket: nyc-duration

aws s3 ls --endpoint-url=http://localhost:4566
2023-07-09 15:58:55 nyc-duration

Q5. % python integration_test.py
The file size is: 3667 bytes

configurable version of batch.py
# export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
# export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"

Q6. Sum of predicted durations for test df: 31.507450372727607