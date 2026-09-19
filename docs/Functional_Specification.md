# Functional Specification

## Serverless HR Lookup Application

**Student:** Nitish Kumar  
**AWS Region:** us-east-1  
**GitHub:** https://github.com/nitishhrms/serverless-hr-lookup

## 1. Purpose

The application provides an authenticated employee lookup portal. A signed-in user enters an Employee ID and receives the matching record from DynamoDB through a protected API. The browser never accesses DynamoDB directly.

## 2. Architecture

The browser calls an API Gateway REST API. `GET /` invokes `hr-ui-function` and returns the HTML, CSS, and JavaScript interface. `GET /employee/{id}` is protected by `SecureHRAuthorizer`. After Cognito validates the ID token, API Gateway invokes `hr-backend-lookup`, which reads the `Employees` DynamoDB table using its IAM execution role.

Architecture diagram: `architecture-diagram.svg`

## 3. Authentication

The application uses Cognito Managed Login with a public SPA client, OAuth 2.0 Authorization Code Grant, and PKCE. The browser creates a code verifier and challenge, receives an authorization code after login, exchanges the code and verifier for tokens, and sends the Cognito ID token in the `Authorization: Bearer` header.

Authentication diagram: `authentication-flow.svg`

## 4. AWS Configuration

| Resource | Configuration |
|---|---|
| API Gateway | `serverless-hr-api`, stage `prod` |
| API URL | `https://ioy99699v8.execute-api.us-east-1.amazonaws.com/prod` |
| UI Lambda | `hr-ui-function` |
| Backend Lambda | `hr-backend-lookup` |
| DynamoDB | `Employees`, partition key `EmployeeID` (String) |
| IAM role | `HRBackendLambdaRole`, `dynamodb:GetItem` only |
| User Pool ID | `us-east-1_yLlaBkBX6` |
| App Client ID | `6v46kadj8g17udr54i6j2a50vb` |
| Managed Login domain | `https://us-east-1yllabkbx6.auth.us-east-1.amazoncognito.com` |
| Cognito user `sub` | `24b88468-2061-7078-20b0-97ee47d4926c` |

## 5. Data Model

The `Employees` table contains `EmployeeID`, `Name`, `Salary`, `DateOfJoin`, and `Description`. `EmployeeID` is the key used for the backend lookup. `Description` is stored as a string. Employee `1005` represents the student and contains the student's IAM user ARN.

## 6. Test Results

| Test | Result |
|---|---|
| Application access | Completed; UI opens over HTTPS |
| Cognito authentication | Completed; Managed Login and PKCE work |
| Valid employee `1001` | Completed; Alice Chan record displayed |
| Student employee `1005` | Completed; Nitish Kumar and IAM user ARN displayed |
| Invalid employee `99999` | Completed; `Employee not found` displayed |
| Unauthorized API request | Completed; API returns `401 Unauthorized` |

Evidence status: all required screenshots are organized in the final submission folder, including the successful-login and employee-1001 screenshots with the browser URL bar visible.

## 7. Source and Evidence

- GitHub source repository: `https://github.com/nitishhrms/serverless-hr-lookup`
- API Gateway export: `api-export.json`
- Architecture diagram: `architecture-diagram.svg`
- Authentication flow: `authentication-flow.svg`
- AI assistance record: `docs/ai-tools.md`

### Screenshot evidence index

| File | Evidence |
|---|---|
| `screenshots/01-cognito-users.png` | Cognito users and confirmation status |
| `screenshots/02-public-ui.png` | Public HTTPS application page |
| `screenshots/03-cognito-login.png` | Cognito Managed Login page and OAuth parameters |
| `screenshots/04-successful-login.png` | Successful Cognito sign-in with URL bar |
| `screenshots/05-valid-employee-1001.png` | Valid employee lookup with URL bar |
| `screenshots/06-student-employee-1005.png` | Student name and IAM ARN |
| `screenshots/07-invalid-employee-99999.png` | `Employee not found` behavior |
| `screenshots/08-unauthorized-api.png` | API rejects request without a token |
| `screenshots/09-api-authorizer.png` | API Gateway authorizer configuration |
| `screenshots/10-cognito-pool.png` | User Pool configuration |
| `screenshots/11-dynamodb-student-item.png` | Required DynamoDB fields and student ARN |
| `screenshots/12-lambda-functions.png` | UI and backend Lambda functions |

## 8. Cleanup

After all evidence is captured and submitted, remove or disable assignment-only API Gateway, Lambda, DynamoDB, Cognito, IAM, and EC2 resources as directed by the instructor.
