import json
import boto3
import botocore.exceptions
import datetime
import os 
import time
def lambda_handler(event, context):

    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


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
    print(event)

    if ('body' not in event or event['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    data = json.loads(event['body'])

    """    
    data["appointment_id"]
    data["user_email"]
    data["status"] -> nuevo status not started | in progress | completed | deleted
    
    Parametros 
    """

    try:
        lambda_client = boto3.client('lambda', region_name='us-east-1' )
        
        client = boto3.client('dynamodb',
                                region_name='us-east-1')
    except Exception as e:
        print("Connection problem with AWS")
        
        return {
            "statusCode": 400,
            "body": json.dumps({
                "appointment": 'response',
                "message": "Problem connecting with AWS."
                # "location": ip.text.replace("\n", "")
            }),
        }

    
    # try:
    #     # Check if there is an existing booking with the same email
    #     response = client.query(
    #     TableName='smb-appointments-test',
    #     IndexName='email-index',
    #     KeyConditionExpression='#datetime_location = :datetime_location',
    #     ExpressionAttributeNames={
    #         '#datetime_location': 'datetime_location'
    #     },
    #     ExpressionAttributeValues={
    #         ':datetime_location': {'S': data["appointment_id"]}
    #     }
    #     # ProjectionExpression='booking_time'
    #     )
   
    #     print('=============================================================')
    #     print(response['Items'])
    #     print(response['Items'][0])
    #     if 'Items' in response:
    #         print("Items found")

    #     else:
    #         print("There were no appointments found.")
    #         return 

    
    # except Exception as e:
    #     print(e)

    print(data)

    try:
        print(f"{data['datetime']}_{data['location']}")
        print("INSIDE TRY BLOCK TABLE INSERT")
        response = client.update_item(
        TableName='smb-appointments-test',
        Key={'datetime_location': {'S': str(f"{data['datetime']}_{data['location']}")},
            'type': {'S': data['type']  }},
        UpdateExpression=f"SET {data['step']} = :new_status",
        ConditionExpression='mail = :existing_email',
        ExpressionAttributeValues={
            ':existing_email': {'S': data["email"] },
            ':new_status': {'S': data["status"] }
        }
        )
        print(response)
        print("RESPONSE:" + str(response))
        print("PUT RESPONSE")
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            pass
            # Invoke the email sending Lambda function asynchronously
            # try:
            #     email_send = lambda_client.invoke(
            #         FunctionName= os.environ.get('SendEmailFunctionName'),
            #         InvocationType='Event',
            #         Payload=json.dumps({
            #              "body": json.dumps({
            #                 "email": data["email"],
            #                 "message": "El email fue enviado exitosamente."

            #         })}
            #         )
            #     )
            #     print(email_send)
            #     print("sent email response")
            # except Exception as e:
            #     print(e)
            #     pass
            #      return {
            #     "statusCode": 400,
            #     "body": json.dumps({
            #         "message": "Lo sentimos.Ha ocurrido un error al enviar el email."
            #     }),
            # }
    except botocore.exceptions.ClientError as e:
        print(e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Lo sentimos. No se pudo modificar el estado."
                # "location": ip.text.replace("\n", "")
            }),
         }
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Lo sentimos.Ha ocurrido un error."
                # "location": ip.text.replace("\n", "")
            }),
         }

    except Exception as e:
        print(e)
        return {
        "statusCode": 200,
        "body": json.dumps({
            "appointment": 'response',
            "message": "Ha ocurrido un error inesperado. Intente nuevamente."
            # "location": ip.text.replace("\n", "")
        }),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "appointment": 'response',
            "message": "El estado del trámite fue actualizado exitosamente."
            # "location": ip.text.replace("\n", "")
        }),
    }