import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        table = dynamodb.Table(TABLE_NAME)
        
        # Get requestId from path parameters
        request_id = event.get('pathParameters', {}).get('requestId')
        
        if not request_id:
            return {
                'statusCode': 400,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps({'error': 'Missing requestId in path'})
            }

        response = table.get_item(
            Key={'requestId': request_id}
        )

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps({'error': 'Request not found'})
            }

        item = response['Item']
        
        # Convert Decimal types to float/int for JSON serialization
        # (Simple hack for this demo, usually use a custom serializer)
        for k, v in item.items():
            if str(type(v)) == "<class 'decimal.Decimal'>":
                 item[k] = float(v)

        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps(item)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'error': str(e)})
        }
