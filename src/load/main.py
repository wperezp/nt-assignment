import os
import boto3
import pandas as pd
import psycopg2

if __name__ == '__main__':
    print(os.environ)
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASS']
    conn = psycopg2.connect(host=db_host, database='postgres', user=db_user, password=db_pass)
    s3_bucket = os.environ['S3_DATA_BUCKET']
    df = pd.read_csv(f's3://{s3_bucket}/landing/fire_data.csv')
    df.head(10)