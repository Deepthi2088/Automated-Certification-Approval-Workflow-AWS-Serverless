# Automated Certification Approval Workflow — AWS Serverless

## Prerequisites
- An active AWS Account.
- Access to the AWS Console.
## 1. System Architecture Overview 



## Step 1: Create DynamoDB Table

1. Go to the **DynamoDB** console.
2. Click **Create table**.
3. **Table name**: `CertificationRequests`
4. **Partition key**: `requestId` (String)
5. Leave other settings as default and click **Create table**.
6. Wait for the table to become active.

## Step 2: Create IAM Role for Lambda

1. Go to the **IAM** console.
2. Click **Roles** -> **Create role**.
3. Select **AWS service** and choose **Lambda**.
4. Click **Next** for permissions.
5. Add the following permissions policies (search and check):
   - `AmazonDynamoDBFullAccess`
   - `AWSStepFunctionsFullAccess` 
   - `CloudWatchLogsFullAccess`
6. Click **Next**.
7. **Role name**: `CertificationLambdaRole`
8. Click **Create role**.

## Step 3: Create Lambda Functions

You will create 4 functions. For each function:
- **Runtime**: Python 3.4 (or latest)
- **Architecture**: x86_64
- **Execution role**: Use an existing role -> `CertificationLambdaRole`

### 3.1 Function: `SubmitRequestFunction`
1. Create function named `SubmitRequestFunction`.
2. **Configuration** -> **Environment variables**:
   - Key: `STATE_MACHINE_ARN`
   - Value: *(Leave blank for now, we will update this later)*

### 3.2 Function: `NotifyManagerFunction`
1. Create function named `NotifyManagerFunction`.
   
### 3.3 Function: `HandleApprovalFunction`
1. Create function named `HandleApprovalFunction`.

### 3.4 Function: `CheckStatusFunction`
1. Create function named `CheckStatusFunction`.
2. **Configuration** -> **Environment variables**:
   - Key: `TABLE_NAME`
   - Value: `CertificationRequests`

## Step 4: Create Step Functions State Machine

1. Go to the **Step Functions** console.
2. Click **Create state machine**.
3. Select **Blank** template or **Write your workflow in code**.
4. In the code editor, replace everything with the content of .
5. **CRITICAL**: You must update the placeholders in the JSON with your actual resource names/ARNs:
   - Replace `${DynamoDBTableName}` with `CertificationRequests` (appears twice).
   - Replace `${NotifyManagerFunctionName}` with `NotifyManagerFunction` (or the full ARN if cross-account, but function name works if in same account).
6. Click **Next**.
7. **Name**: `ApprovalStateMachine`
8. **Permissions**: Select **Create a new role** (Step Functions will automatically add permission to invoke Lambda and access DynamoDB based on your definition).
9. Click **Create state machine**.
10. **Copy the ARN** of the created State Machine (e.g., `arn:aws:states:us-east-1:123456789012:stateMachine:ApprovalStateMachine`).

## Step 5: Update Lambda Configuration

1. Go back to **Lambda** console -> `SubmitRequestFunction`.
2. **Configuration** -> **Environment variables**.
3. Update `STATE_MACHINE_ARN` with the ARN you just copied.
4. Click **Save**.

## Step 6: Create API Gateway

1. Go to **API Gateway** console.
2. Click **Create API** -> **HTTP API** (Build).
3. **API name**: `CertificationAPI`.
4. **Integrations**: You can add them now or later. Let's add them now.
   - Integration targets: Lambda
   - Choose `SubmitRequestFunction`, `HandleApprovalFunction`, `CheckStatusFunction`.
5. **Configure routes**:
   - `POST /request` -> `SubmitRequestFunction`
   - `POST /approval` -> `HandleApprovalFunction`
   - `GET /request/{requestId}` -> `CheckStatusFunction`
6. Click **Next** (Stages) -> Leave as `$default`.
7. Click **Create**.
9. Note the **Invoke URL** (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com`).


## Verification Steps

1. **Submit a Request**:
   ```bash
   curl -X POST https://<YOUR-API-URL>/request \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "course": "AWS Certified Developer", "cost": 150}'
   ```
   *Response*: `{"requestId": "uuid...", "executionArn": "..."}`

2. **Check Logs for Token**:
   - Go to CloudWatch Logs for `NotifyManagerFunction`.
   - Find the log entry `APPROVAL TOKEN: ...`. Copy the long token string.

3. **Check Status (Pending)**:
   ```bash
   curl https://<YOUR-API-URL>/request/<REQUEST-ID>
   ```
   *Response*: `{"status": "PENDING", ...}`

4. **Approve Request**:
   ```bash
   curl -X POST https://<YOUR-API-URL>/approval \
     -H "Content-Type: application/json" \
     -d '{"requestId": "<REQUEST-ID>", "decision": "APPROVED", "taskToken": "<PASTE-TOKEN-HERE>"}'
   ```

5. **Verify Status (Approved)**:
   ```bash
   curl https://<YOUR-API-URL>/request/<REQUEST-ID>
   ```
   *Response*: `{"status": "APPROVED", ...}`

.
