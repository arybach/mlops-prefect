import pandas as pd

def column_mods(df):
    # Step 1: Convert columns to datetime
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # Step 1: Calculate trip duration
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    
    # Step 3: Create "weekend or workday" column
    # Mapping weekdays to "workday"
    df.loc[df['tpep_pickup_datetime'].dt.weekday.isin([0, 1, 2, 3, 4]), 'weekend_or_workday'] = 'workday'

    # Mapping Saturday and Sunday to "weekend"
    df.loc[df['tpep_pickup_datetime'].dt.weekday.isin([5, 6]), 'weekend_or_workday'] = 'weekend'

    # Step 4: Create "time of the day" column
    df.loc[df['tpep_pickup_datetime'].dt.hour.between(6, 17), 'time_of_day'] = 'day'
    df.loc[~df['tpep_pickup_datetime'].dt.hour.between(6, 17), 'time_of_day'] = 'night'

    return df