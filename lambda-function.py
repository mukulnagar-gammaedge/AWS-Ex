import boto3
import os
import json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageMetadata')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        response = s3.head_object(Bucket=bucket, Key=key)
        metadata = {
            'ImageID': key,
            'Bucket': bucket,
            'Size': response['ContentLength'],
            'Timestamp': str(response['LastModified'])
        }
        table.put_item(Item=metadata)
    return {'statusCode': 200, 'body': json.dumps('Metadata saved')}
