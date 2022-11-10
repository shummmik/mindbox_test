import pandas as pd
from pandas import DataFrame
from datetime import timedelta

THREE_MIN = timedelta(minutes=3)


def add_session(df: DataFrame) -> DataFrame:
    df['timestamp'] = pd.to_datetime(df.timestamp)
    df.sort_values(by=['customer_id', 'timestamp'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['session_id'] = (((df['timestamp'] - df.groupby('customer_id') \
                          .timestamp.shift(1) \
                          .fillna(pd.Timestamp(0, tz=0))) > THREE_MIN) * 1)
    df['session_id'] = df.session_id.expanding().sum().astype(int)
    return df
