import json
import uuid
import boto3
import os
import datetime

# Initialize the Step Functions client
sfn_client = boto3.client('stepfunctions')

# Environment variable for the State Machine ARN
STATE_MACHINE_ARN = os.environ.get('STATE_MACHINE_ARN')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
        # Parse the input body
        # API Gateway passes data in 'body', but if testing in console it might be raw
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        # Validate input
        required_fields = ['name', 'course', 'cost']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps({'error': f'Missing field: {field}'})
                }

        # Generate a unique Request ID
        request_id = str(uuid.uuid4())
        
        # Prepare input for Step Functions
        sfn_input = {
            'requestId': request_id,
            'name': body['name'],
            'course': body['course'],
            'cost': body['cost'],
            'requestDate': datetime.datetime.now().isoformat()
        }

        # Start the Step Functions execution
        if not STATE_MACHINE_ARN:
            raise Exception("STATE_MACHINE_ARN environment variable is not set")

        response = sfn_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=request_id, # Use request ID as execution name for easy lookup
            input=json.dumps(sfn_input)
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'message': 'Request submitted successfully',
                'requestId': request_id,
                'executionArn': response['executionArn']
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': str(e)})
        }
