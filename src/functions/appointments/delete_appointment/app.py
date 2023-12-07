import json
import boto3
import botocore.exceptions
import datetime
import os 

def lambda_handler(event, context):

    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """


    if ('body' not in event or event['httpMethod'] != 'DELETE'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    
    data = json.loads(event['body'])
    data["appointment_id"]
    
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    client = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                endpoint_url= "https://dynamodb.us-east-1.amazonaws.com")
    
   
    print(data)
    try:
        response = client.delete_item(
        TableName='appointments',
        Key={
            'string': 'string'
        }
        )
    except botocore.exceptions.ClientError as e:
        return {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Ha ocurrido un error al borrar el turno."
            # "location": ip.text.replace("\n", "")
        }),
        }



    return {
        "statusCode": 200,
        "body": json.dumps({
            "appointment": 'response',
            "message": "El turno fue borrado exitosamente."
            # "location": ip.text.replace("\n", "")
        }),
    }
