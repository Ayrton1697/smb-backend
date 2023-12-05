import json
import boto3
import botocore.exceptions
import datetime

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


    if ('body' not in event or event['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    data = json.loads(event['body'])


    client = boto3.client('dynamodb',
                              region_name='us-east-1',
                              aws_access_key_id='AKIAQWEIXVN6RBKUF5RG',
                              aws_secret_access_key='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',
                              endpoint_url= "https://dynamodb.us-east-1.amazonaws.com")
    
    try:
        # Check if there is an existing booking with the same email
        response = client.query(
        TableName='appointments',
        IndexName='email-index',
        KeyConditionExpression='#mail = :email',
        ExpressionAttributeNames={
            '#mail': 'mail'
        },
        ExpressionAttributeValues={
            ':email': {'S': data["email"]}
        }
        # ProjectionExpression='booking_time'
        )
        time_difference = []
        print(response)
        print(response['Items'])
        print(response['Items'][0])
        if 'Items' in response:
            # Get the timestamp of the first booking
            first_booking_time = datetime.datetime.strptime(response['Items'][0]['TIME']['S'], '%Y-%m-%d %H:%M')
        
            # Calculate the current timestamp
            current_time = datetime.datetime.now()

            # Calculate the difference between the current timestamp and the first booking timestamp
            time_difference = current_time - first_booking_time

        # Check if the time difference is within the allowed range of 30 days
        if time_difference.days <= 30:
            return {
                'statusCode': 400,
                'headers': {},
                'body': json.dumps({'message': 'Lo sentimos. Ya existe una reserva para ese correo en los proximos 30 días.'})
            }
    except Exception as e:
        pass

    
    print(data)
    try:
        response = client.put_item(
        TableName='appointments',
        Item={
            'USER_ID' : {
            'N': data["user_id"]
                },
            'user_phone_number' : {
            'N': data["user_phone_number"]
                },
            'appointment_id' : {
            'N': data["appointment_id"]
                },
            'TIME' : {
                'S': data["appointment_datetime"]
                },
            'description' : {
                'S': data["description"]
                },
            'optionals' : {
                'S': data["optionals"]
                },
            'ref_code' : {
                'S': data["ref_code"]
                },
            'type' : {
                'S': data["type"]
                },
            'mail' : {
                'S': data["email"]
                },
            'CLIENT_ID' : {
                'S': data["client_id"]
                },
        },
        ConditionExpression='mail = :empty_value AND mail <> :dup_value',
        ExpressionAttributeValues={
            ':empty_value': {'S': ""},
            ':dup_value': {'S': data["email"] },
        }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Lo sentimos.Ese horario ya se encuentra reservado."
                # "location": ip.text.replace("\n", "")
            }),
         }



    return {
        "statusCode": 200,
        "body": json.dumps({
            "appointment": 'response',
            "message": "El turno fue creado exitosamente."
            # "location": ip.text.replace("\n", "")
        }),
    }
