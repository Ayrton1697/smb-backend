import json
import boto3



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
    user_id = params["id-testing"]

    client = boto3.client('dynamodb',
                              region_name='us-east-1',
                              aws_access_key_id='AKIAQWEIXVN6RBKUF5RG',
                              aws_secret_access_key='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',
                              endpoint_url= "https://dynamodb.us-east-1.amazonaws.com")
    
   

    item = client.put_item(
    Key={
        'id': {
            'N': str(user_id),
        }
    },
    TableName='smb-users',
)

    # print(json.dumps(response))


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": item,
            # "location": ip.text.replace("\n", "")
        }),
    }
