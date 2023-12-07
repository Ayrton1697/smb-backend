import json
import boto3
import os 

def lambda_handler(event, context):

    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    print(json.loads(event.get("body")))
  
    client = boto3.client("ses", region_name='us-east-1',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,)

    try:
        print(json.loads(event.get("body")))
        print(json.loads(event.get("body"))["message"])
        subject = "EPAS Booking Confirmation"
        body = json.loads(event.get("body"))["message"]
        referrer = json.loads(event.get("body"))["email"]
        
        message={'Subject': {'Data': subject},'Body': {'Text': {'Data': body},'Html': {'Data': body} } }
        
        response = client.send_email(
        Source = "founders@leantk.com", Destination = {"ToAddresses": [referrer]}, Message = message, ReplyToAddresses = [referrer]
        )
        
        # TODO implement
        # return response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': "El email ha sido enviado correctamente."
                }
            )
        }
    except Exception as e:
        return {
    'statusCode': 400,
    'headers': {
        'Content-Type': 'application/json; charset=utf-8',
        'X-My-Header': 'whatever',
        'Access-Control-Allow-Methods': 'GET,OPTIONS,POST',
        'Access-Control-Allow-Origin': 'https://www.leantk.com'
    },
    'body': json.dumps({
        'message': 'Ha ocurrido un error al enviar el email.'
        }
    )
}

