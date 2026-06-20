import boto3
import uuid
import os
import json
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    bucket_name = os.environ["BUCKET_NAME"]
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    # Guardar en S3 (Push ingestion)
    filename = f"comentarios/{datetime.now().isoformat()}_{uuidv1}.json"
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=json.dumps(comentario),
        ContentType='application/json'
    )
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response,
        's3_file': filename
    }
