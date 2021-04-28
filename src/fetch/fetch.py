import boto3
import os
import requests


def lambda_handler(event, context):
    fire_data_url = os.environ['FIRE_DATA_URL']
    response = requests.get(fire_data_url)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ['S3_DATA_BUCKET'])
    bucket.put_object(Key=f'landing/fire_data.csv', Body=response.content)
