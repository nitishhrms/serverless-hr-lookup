import json

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SecureHR Employee Portal</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #172033;
}

.header {
    background: #082b59;
    color: white;
    padding: 18px 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

.logo span {
    color: #54a8ff;
}

.login-button {
    background: white;
    color: #082b59;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
}

.hero {
    background: linear-gradient(135deg, #082b59, #1261a0);
    color: white;
    padding: 55px 8%;
}

.hero h1 {
    margin: 0 0 12px;
    font-size: 38px;
}

.hero p {
    margin: 0;
    font-size: 17px;
    opacity: 0.9;
}

.container {
    max-width: 900px;
    margin: -35px auto 50px;
    padding: 0 20px;
}

.card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 25px;
}

.card h2 {
    margin-top: 0;
    color: #082b59;
}

.search-row {
    display: flex;
    gap: 12px;
}

input {
    flex: 1;
    padding: 14px;
    border: 1px solid #c5ceda;
    border-radius: 5px;
    font-size: 16px;
}

.search-button {
    background: #1261a0;
    color: white;
    border: none;
    padding: 14px 25px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
}

.search-button:hover {
    background: #0b4e86;
}

.details {
    display: none;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #e6ebf1;
}

.detail-label {
    font-weight: bold;
    color: #64748b;
}

.detail-value {
    text-align: right;
}

.message {
    margin-top: 15px;
    padding: 12px;
    border-radius: 5px;
    display: none;
}

.error {
    background: #fee2e2;
    color: #991b1b;
}

.success {
    background: #dcfce7;
    color: #166534;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 25px;
    font-size: 14px;
}
</style>
</head>

<body>

<header class="header">
    <div class="logo">Secure<span>HR</span></div>
    <button class="login-button" onclick="login()">Secure Login</button>
</header>

<section class="hero">
    <h1>Employee Information Portal</h1>
    <p>Securely look up employee information using an Employee ID.</p>
</section>

<main class="container">

    <section class="card">
        <h2>Employee Lookup</h2>

        <div class="search-row">
            <input id="employeeId" placeholder="Enter Employee ID, for example 1001">
            <button class="search-button" onclick="searchEmployee()">
                Search
            </button>
        </div>

        <div id="message" class="message"></div>
    </section>

    <section id="details" class="card details">
        <h2>Employee Details</h2>

        <div class="detail-row">
            <span class="detail-label">Employee ID</span>
            <span class="detail-value" id="employeeIdValue"></span>
        </div>

        <div class="detail-row">
            <span class="detail-label">Name</span>
            <span class="detail-value" id="nameValue"></span>
        </div>

        <div class="detail-row">
            <span class="detail-label">Salary</span>
            <span class="detail-value" id="salaryValue"></span>
        </div>

        <div class="detail-row">
            <span class="detail-label">Date of Join</span>
            <span class="detail-value" id="dateOfJoinValue"></span>
        </div>

        <div class="detail-row">
            <span class="detail-label">Description</span>
            <span class="detail-value" id="descriptionValue"></span>
        </div>
    </section>

</main>

<footer class="footer">
    SecureHR Employee Portal | AWS Serverless Application
</footer>

<script>

const API_BASE_URL =
    "https://ioy99699v8.execute-api.us-east-1.amazonaws.com/prod";

const COGNITO_DOMAIN =
    "https://us-east-1yllabkbx6.auth.us-east-1.amazoncognito.com";

const CLIENT_ID =
    "6v46kadj8g17udr54i6j2a50vb";

const REDIRECT_URI =
    "https://ioy99699v8.execute-api.us-east-1.amazonaws.com/prod";

let idToken = sessionStorage.getItem("id_token");

function base64UrlEncode(bytes) {
    let binary = "";

    bytes.forEach(byte => {
        binary += String.fromCharCode(byte);
    });

    return btoa(binary)
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/, "");
}

function randomString(length = 64) {
    const bytes = new Uint8Array(length);
    crypto.getRandomValues(bytes);
    return base64UrlEncode(bytes);
}

async function createCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await crypto.subtle.digest("SHA-256", data);

    return base64UrlEncode(new Uint8Array(digest));
}

async function login() {
    const codeVerifier = randomString(64);
    const codeChallenge = await createCodeChallenge(codeVerifier);
    const state = randomString(32);

    sessionStorage.setItem("code_verifier", codeVerifier);
    sessionStorage.setItem("oauth_state", state);

    const parameters = new URLSearchParams({
        response_type: "code",
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
        scope: "openid email",
        code_challenge_method: "S256",
        code_challenge: codeChallenge,
        state: state
    });

    window.location.href =
        `${COGNITO_DOMAIN}/oauth2/authorize?${parameters.toString()}`;
}

async function handleAuthCallback() {
    const parameters = new URLSearchParams(window.location.search);

    const code = parameters.get("code");
    const returnedState = parameters.get("state");

    if (!code) {
        return;
    }

    const savedState = sessionStorage.getItem("oauth_state");
    const codeVerifier = sessionStorage.getItem("code_verifier");

    if (!savedState || returnedState !== savedState) {
        showMessage("Invalid authentication state.", "error");
        return;
    }

    const tokenResponse = await fetch(
        `${COGNITO_DOMAIN}/oauth2/token`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                grant_type: "authorization_code",
                client_id: CLIENT_ID,
                code: code,
                redirect_uri: REDIRECT_URI,
                code_verifier: codeVerifier
            })
        }
    );

    const tokens = await tokenResponse.json();

    if (!tokenResponse.ok) {
        showMessage("Authentication failed.", "error");
        console.error(tokens);
        return;
    }

    idToken = tokens.id_token;

    sessionStorage.setItem("id_token", idToken);
    sessionStorage.removeItem("code_verifier");
    sessionStorage.removeItem("oauth_state");

    window.history.replaceState(
        {},
        document.title,
        REDIRECT_URI
    );

    showMessage("Successfully signed in.", "success");
}

function logout() {
    sessionStorage.clear();

    const parameters = new URLSearchParams({
        client_id: CLIENT_ID,
        logout_uri: REDIRECT_URI
    });

    window.location.href =
        `${COGNITO_DOMAIN}/logout?${parameters.toString()}`;
}

async function searchEmployee() {
    const employeeId = document
        .getElementById("employeeId")
        .value
        .trim();

    if (!employeeId) {
        showMessage("Please enter an Employee ID.", "error");
        return;
    }

    if (!idToken) {
        showMessage("Please sign in before searching.", "error");
        return;
    }

    const response = await fetch(
        `${API_BASE_URL}/employee/${encodeURIComponent(employeeId)}`,
        {
            headers: {
                "Authorization": `Bearer ${idToken}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        document.getElementById("details").style.display = "none";
        showMessage(data.error || "Employee not found.", "error");
        return;
    }

    document.getElementById("employeeIdValue").textContent =
        data.employeeId;

    document.getElementById("nameValue").textContent =
        data.name;

    document.getElementById("salaryValue").textContent =
        "$" + Number(data.salary).toLocaleString();

    document.getElementById("dateOfJoinValue").textContent =
        data.dateOfJoin;

    document.getElementById("descriptionValue").textContent =
        data.description;

    document.getElementById("details").style.display = "block";

    showMessage("Employee record found.", "success");
}

function showMessage(text, type) {
    const message = document.getElementById("message");

    message.textContent = text;
    message.className = `message ${type}`;
    message.style.display = "block";
}

window.addEventListener("load", handleAuthCallback);

window.login = login;

window.logout = logout;

window.searchEmployee = searchEmployee;

</script>

</body>
</html>
"""

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*"
        },
        "body": HTML
    }