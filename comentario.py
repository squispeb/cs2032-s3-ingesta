import json
import os
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    bucket_name = os.environ['BUCKET_NAME']
    
    filename = f"comentarios/{datetime.now().isoformat()}_{uuid.uuid4()}.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=json.dumps(body),
        ContentType='application/json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Comentario guardado', 'file': filename})
    }
