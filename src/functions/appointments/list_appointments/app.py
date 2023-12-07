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

  
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    client = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                endpoint_url= "https://dynamodb.us-east-1.amazonaws.com")
    
   
    try:
        table_name = "appointments"
        response = client.scan(
            TableName=table_name,
            FilterExpression='mail <> :empty_value',
            ExpressionAttributeValues={
                ':empty_value': {'S': ""}
            })
    
            # Obtener los elementos escaneados
        items = response.get('Items', [])
        

        print(json.dumps(items))

        # print(json.dumps(response))


        return {
            "statusCode": 200,
            "body": json.dumps({
                "appointments": items,
            }),
        }
    except Exception as e:
          
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

