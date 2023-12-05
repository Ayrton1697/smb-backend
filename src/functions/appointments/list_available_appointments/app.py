import json
import boto3

# Configuración de las credenciales de AWS
aws_access_key_id = 'AKIAQWEIXVN6Q6WSENFZ'
aws_secret_access_key = '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'
aws_region = 'us-east-1'  # Reemplaza con la región de tu tabla DynamoDB
table_name = 'appointments'

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

# Obtener la referencia a la tabla
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Escanear la tabla DynamoDB para obtener todas las filas con USER_ID vacío
        response = table.scan(
            FilterExpression='USER_ID = :user_id',
            ExpressionAttributeValues={':user_id': ''}
        )

        # Obtener los elementos escaneados
        items = response.get('Items', [])

        # Imprimir los elementos encontrados
        for item in items:
            print(json.dumps(item))

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
