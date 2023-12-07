import json
import boto3
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

    params = event["queryStringParameters"]
    user_id = params["user_id"]
    client_id = params["client_id"]
    appointment_datetime = params["appointment_datetime"]
  
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    client = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                endpoint_url= "https://dynamodb.us-east-1.amazonaws.com")
    
   

    item = client.get_item(
    Key={
        'id': {
            'N': str(user_id),
        }
    },
    TableName='appointments',
)

    # print(json.dumps(response))


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": item,
            # "location": ip.text.replace("\n", "")
        }),
    }
