import json
import boto3
import os

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # event will contain the Input from the Step Function state, including the Task Token
    # passed via Parameters in the definition
    
    try:
        task_token = event.get('taskToken')
        request_id = event.get('requestId')
        name = event.get('name')
        course = event.get('course')
        cost = event.get('cost')

        if not task_token:
            print("Error: No taskToken provided in event")
            # We don't fail, just log
            return {'status': 'Error: No taskToken'}

        print(f"--- ACTION REQUIRED ---")
        print(f"Request ID: {request_id}")
        print(f"Employee: {name}")
        print(f"Course: {course}")
        print(f"Cost: ${cost}")
        print(f"APPROVAL TOKEN: {task_token}")
        print(f"--- Copy the above token to approve/reject the request ---")

        # In a real app, you would send an email with a link like:
        # https://api-url/approve?token=...
        # Here we just log it for the manual demo.
        
        return {
            'status': 'NotificationSent',
            'message': 'Check CloudWatch Logs for the Task Token'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
