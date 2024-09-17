# fcm.py
import json
import requests
from firebase_admin import messaging, credentials, initialize_app
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.conf import settings
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'notificat/firbase.json')
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIAL)
initialize_app(cred)

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        FIREBASE_ADMIN_CREDENTIAL, scopes=SCOPES)
    request = Request()
    credentials.refresh(request)
    return credentials.token



def subscribe_user_to_topic(token, topic):
    url = f'https://iid.googleapis.com/iid/v1/{token}/rel/topics/{topic}'
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers)
    print("oooooooooooo")
    print(response)
    return response.json()

def send_fcm_message_to_topic(topic, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic
    )
    response = messaging.send(message)
    return response

def send_fcm_message_to_token(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token
    )
    response = messaging.send(message)
    return response
