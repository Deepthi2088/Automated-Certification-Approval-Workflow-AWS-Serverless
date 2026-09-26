import json
import boto3
import os

sfn_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        task_token = body.get('taskToken')
        decision = body.get('decision') # 'APPROVED' or 'REJECTED'

        if not task_token or not decision:
            return {
                'statusCode': 400,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps({'error': 'Missing taskToken or decision'})
            }
        
        if decision not in ['APPROVED', 'REJECTED']:
             return {
                'statusCode': 400,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps({'error': 'decision must be APPROVED or REJECTED'})
            }

        output = json.dumps({
            'status': decision,
            'processedAt': 'ManualApproval'
        })
        
        print(f"Sending Task {decision} for token: {task_token}...")

        sfn_client.send_task_success(
            taskToken=task_token,
            output=output
        )

        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'message': f'Request {decision} successfully'})
        }

    except sfn_client.exceptions.TaskDoesNotExist:
         return {
            'statusCode': 404,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'error': 'Task Token not found or expired'})
        }
    except sfn_client.exceptions.InvalidToken:
         return {
            'statusCode': 400,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'error': 'Invalid Task Token'})
        }
    except sfn_client.exceptions.TaskTimedOut:
         return {
            'statusCode': 410,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'error': 'Task Timed Out'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'error': str(e)})
        }
