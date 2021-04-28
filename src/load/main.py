import os
import pandas as pd
from sqlalchemy import create_engine

import transform

if __name__ == '__main__':
    print(os.environ)
    # Create sqlalchemy connection
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASS']
    conn_string = 'postgresql://{0}:{1}@{2}:5432/postgres'.format(db_user, db_pass, db_host)
    db_engine = create_engine(conn_string)
    # conn = psycopg2.connect(host=db_host, database='postgres', user=db_user, password=db_pass)
    # Get last retrieved data
    s3_bucket = os.environ['S3_DATA_BUCKET']
    df_source = pd.read_csv(f's3://{s3_bucket}/landing/fire_data.csv')
    print(df_source.head(10))
    transform.transform_data(df_source, db_engine)
