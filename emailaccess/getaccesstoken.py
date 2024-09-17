import requests

url = "https://accounts.zoho.com/oauth/v2/token"
payload = {
    "code": "1000.b3a746c41bbe3382c7307ae090b18f3e.794d03016f3317ce33a7bbeacb5a6151",
    'redirect_uri': 'http://127.0.0.1:8090',
    'client_id': '1000.X7QKPWVBWTMPZXX052742CWHO8PT0B',
    'client_secret': '7296dca99581aaac8f9d4427755c1f05b88e0bf1f0',
    'grant_type': 'authorization_code',
    'scope':'ZohoMail.messages.ALL'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, data=payload, headers=headers)
response.raise_for_status()
print(response.json())
