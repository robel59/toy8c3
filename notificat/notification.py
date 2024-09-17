import argparse
import json
import requests
import google.auth.transport.requests
from google.oauth2 import service_account
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'notificat/firbase.json')

PROJECT_ID = 'zufan-58a81'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def _get_access_token():
  credentials = service_account.Credentials.from_service_account_file(
    FIREBASE_ADMIN_CREDENTIAL, scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token


def sendNotfication(title, message_body, token):
  fcm_message = {
    'message': {
      'token':token,
    'notification': {
      'title': title,
      'body': message_body
    }
    }
  }
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)


