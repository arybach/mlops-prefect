#FROM arybach/ride-duration-predict:v1
FROM svizor/zoomcamp-model:mlops-3.10.0-slim

WORKDIR /app

RUN pip install pandas pyarrow fastparquet scikit-learn==1.2.2

COPY stutter_docker.py .

# Run the script and output the mean predicted duration for April 2022
CMD ["python", "stutter_docker.py", "--year", "2022", "--month", "4", "--taxi_type", "green"]

# docker build -t ride-duration-predict:v2 .
# docker run ride-duration-predict:v2