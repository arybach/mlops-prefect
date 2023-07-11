# added main and split read_data function into fetch_data and test_prepare_data functions
import sys, os
import pickle
import pandas as pd
from datetime import datetime
import pandas as pd
import numpy as np

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)

def fetch_data():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]
    columns = ['PULocationID', 'DOLocationID',
               'tpep_pickup_datetime', 'tpep_dropoff_datetime']

    df = pd.DataFrame(data, columns=columns)
    return df

def read_data(filename, categorical):

    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


def test_prepare_data():

    categorical = ['PULocationID', 'DOLocationID']

    expected_output = [
        {'PULocationID': np.nan, 'DOLocationID': np.nan, 'tpep_pickup_datetime': dt(1, 2),
        'tpep_dropoff_datetime': dt(1, 10)},
        {'PULocationID': 1, 'DOLocationID': np.nan, 'tpep_pickup_datetime': dt(1, 2),
        'tpep_dropoff_datetime': dt(1, 10)},
        {'PULocationID': 1, 'DOLocationID': 2, 'tpep_pickup_datetime': dt(2, 2),
        'tpep_dropoff_datetime': dt(2, 3)},
        {'PULocationID': np.nan, 'DOLocationID': 1, 'tpep_pickup_datetime': dt(1, 2, 0),
        'tpep_dropoff_datetime': dt(1, 2, 50)},
        {'PULocationID': 2, 'DOLocationID': 3, 'tpep_pickup_datetime': dt(1, 2, 0),
        'tpep_dropoff_datetime': dt(1, 2, 59)},
        {'PULocationID': 3, 'DOLocationID': 4, 'tpep_pickup_datetime': dt(1, 2, 0),
        'tpep_dropoff_datetime': dt(2, 2, 1)},
    ]

    expected_df = pd.DataFrame(expected_output)
    # Compare the resulting DataFrame with the expected DataFrame
    result_df = fetch_data()
    assert result_df.equals(expected_df)

    expected_df['duration'] = expected_df.tpep_dropoff_datetime - expected_df.tpep_pickup_datetime
    expected_df['duration'] = expected_df.duration.dt.total_seconds() / 60

    expected_df = expected_df[(expected_df.duration >= 1) & (expected_df.duration <= 60)].copy()

    expected_df[categorical] = expected_df[categorical].fillna(-1).astype('int').astype('str')

    return expected_df


def predict_test_data(df, year, month):
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    return df_result


def main(year, month):
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet'
    output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    categorical = ['PULocationID', 'DOLocationID']

    df = read_data(input_file, categorical)
    df_result = predict_test_data(df, year, month)

    df_result.to_parquet(output_file, engine='pyarrow', index=False)


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    df_fetch = test_prepare_data()
    df_fetch.to_parquet('output/fetch_df.parquet', engine='pyarrow', compression=None, index=False)

    df_test = test_prepare_data()
    df_test.to_parquet('output/test_df.parquet', engine='pyarrow', compression=None, index=False)
    
    main(year, month)