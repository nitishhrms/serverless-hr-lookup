SecureHR Serverless HR Lookup

SecureHR is an authenticated serverless employee lookup application built with Amazon API Gateway, AWS Lambda, Amazon DynamoDB, Amazon Cognito, and AWS IAM.

The application allows an authenticated user to enter an Employee ID and retrieve the corresponding employee record. The browser never accesses DynamoDB directly.

Architecture

User Browser
    |
    | HTTPS
    v
API Gateway REST API
    |
    |-- GET / ----------------------> UI Lambda
    |                                  Returns HTML, CSS, and JavaScript
    |
    |-- GET /employee/{id}
            |
            v
       Cognito Authorizer
            |
            | Valid ID token
            v
       Backend Lambda
            |
            | IAM execution role
            v
       DynamoDB Employees table

Authentication uses Cognito Managed Login, OAuth 2.0 Authorization Code Grant, and PKCE.

AWS services

Service

Purpose

Amazon API Gateway

Provides HTTPS REST API routes

AWS Lambda

Runs the UI and backend code without managing servers

Amazon DynamoDB

Stores employee records

Amazon Cognito

Authenticates users through Managed Login

AWS IAM

Controls Lambda permissions

API routes

Public route

GET /

Returns the SecureHR web interface.

Protected route

GET /employee/{id}
Authorization: Bearer <Cognito ID token>

Returns the employee record for the requested Employee ID.

Example response:

{
  "employeeId": "1001",
  "name": "Alice Chan",
  "salary": 92000,
  "dateOfJoin": "2024-01-15",
  "description": "Cloud Engineering employee"
}

AWS configuration

Resource

Configuration

API Gateway

serverless-hr-api, stage prod

Application URL

https://ioy99699v8.execute-api.us-east-1.amazonaws.com/prod

UI Lambda

hr-ui-function

Backend Lambda

hr-backend-lookup

DynamoDB table

Employees

Partition key

EmployeeID as String

IAM role

HRBackendLambdaRole

IAM permission

dynamodb:GetItem on Employees only

Cognito User Pool

us-east-1_yLlaBkBX6

Cognito App Client

6v46kadj8g17udr54i6j2a50vb

Managed Login domain

https://us-east-1yllabkbx6.auth.us-east-1.amazoncognito.com

DynamoDB data model

Each employee item contains:

EmployeeID   String  Partition key
Name         String
Salary       Number
DateOfJoin   String
Description  String

Employee 1005 represents the student:

Name: Nitish Kumar
Description: arn:aws:iam::699038657389:user/nitish-student

Authentication flow

The user clicks Secure Login.

The browser creates a PKCE code verifier and code challenge.

Cognito Managed Login authenticates the user.

Cognito returns a temporary authorization code.

The browser exchanges the code and verifier for tokens.

The browser sends the Cognito ID token to API Gateway.

The Cognito authorizer validates the token.

API Gateway invokes the backend Lambda only after successful validation.

Deployment summary

The application was deployed using the AWS Management Console:

Create the DynamoDB Employees table.

Add sample employee records.

Create the least-privilege IAM policy and Lambda execution role.

Deploy hr-backend-lookup.

Deploy hr-ui-function.

Create API Gateway resources and Lambda proxy integrations.

Create the Cognito User Pool and public application client.

Configure Managed Login and the HTTPS callback URL.

Create SecureHRAuthorizer in API Gateway.

Protect GET /employee/{id} with the authorizer.

Deploy the API to the prod stage.

Testing

Test

Expected result

Open the application URL

SecureHR UI loads over HTTPS

Sign in through Cognito

User successfully authenticates

Search Employee ID 1001

Alice Chan record is displayed

Search Employee ID 1005

Student record and IAM ARN are displayed

Search Employee ID 99999

Employee not found is displayed

Call /employee/1001 without a token

API returns 401 Unauthorized

Screenshots and AWS configuration evidence are available in screenshots/.

Repository structure

backend/
└── lambda_function.py

ui/
└── lambda_function.py

docs/
├── Functional_Specification.md
├── Functional_Specification_Serverless_HR.pdf
├── architecture-diagram.svg
├── authentication-flow.svg
├── api-export.json
└── ai-tools.md

screenshots/
└── AWS configuration and testing evidence

Security considerations

The browser does not access DynamoDB directly.

The backend Lambda uses an IAM role instead of embedded AWS credentials.

The IAM role is limited to dynamodb:GetItem for the employee table.

The employee API requires a valid Cognito ID token.

The Cognito application client is public and uses PKCE; no client secret is stored.

AWS access keys, passwords, tokens, and authorization codes must never be committed to GitHub.

AI assistance

AI assistance was used to explain AWS services, draft and debug application code, troubleshoot authentication and API behavior, create diagrams, and organize documentation. The AWS resources, configuration, testing, and final review were completed by the student.

Additional details are available in docs/ai-tools.md.

Cleanup

After the assignment is submitted and the instructor has accepted the evidence, remove assignment-only resources to avoid unnecessary charges:

API Gateway REST API

Lambda functions

DynamoDB table

Cognito User Pool

Assignment-specific IAM role and policy

EC2 instance and attached storage, if used

Author

Nitish Kumar
GitHub: https://github.com/nitishhrms/serverless-hr-lookup