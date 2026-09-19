\# Serverless HR Lookup Application



An authenticated employee lookup application built with AWS Lambda, API Gateway,

Cognito, DynamoDB, and IAM.



\## Architecture



Browser → API Gateway REST API → Cognito Authorizer → Backend Lambda → DynamoDB



The public `GET /` route returns the web interface through the UI Lambda.

The protected `GET /employee/{id}` route retrieves employee data.



\## AWS Resources



\- Region: `us-east-1`

\- API Gateway URL: `https://ioy99699v8.execute-api.us-east-1.amazonaws.com/prod`

\- DynamoDB table: `Employees`

\- DynamoDB partition key: `EmployeeID`

\- Backend Lambda: `hr-backend-lookup`

\- UI Lambda: `hr-ui-function`

\- Cognito User Pool ID: `us-east-1\_yLlaBkBX6`

\- Cognito App Client ID: `6v46kadj8g17udr54i6j2a50vb`

\- Cognito Managed Login domain: `https://us-east-1yllabkbx6.auth.us-east-1.amazoncognito.com`



\## Authentication



The application uses Cognito Managed Login with OAuth 2.0 Authorization Code

Grant and PKCE. The browser sends the Cognito ID token in the Authorization

header when calling the protected employee API.



\## Testing



\- Employee `1001`: valid employee record

\- Employee `1005`: student record

\- Employee `99999`: `Employee not found`

\- Unauthenticated API access: `401 Unauthorized`



\## Security



The backend Lambda uses an IAM execution role with only

`dynamodb:GetItem` permission on the `Employees` table.



No AWS credentials, passwords, client secrets, or authentication tokens are

included in this repository.



\## AI Assistance



AI assistance was used to explain AWS concepts, debug Lambda and API Gateway

configuration, review authentication flow, and prepare documentation.

All AWS resources were configured and tested by the student.

