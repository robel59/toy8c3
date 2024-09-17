

import argparse
import json
import requests
import google.auth.transport.requests

from google.oauth2 import service_account

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'notificat/firbase.json')

PROJECT_ID = 'zufan-58a81'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']



# [START retrieve_access_token]
def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = service_account.Credentials.from_service_account_file(
    FIREBASE_ADMIN_CREDENTIAL, scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token
# [END retrieve_access_token]

def _send_fcm_message(fcm_message):
  """Send HTTP request to FCM with given message.

  Args:
    fcm_message: JSON object that will make up the body of the request.
  """
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

def _build_common_message():
  """Construct common notifiation message.

  Construct a JSON object that will be used to define the
  common parts of a notification message that will be sent
  to any app instance subscribed to the news topic.
  """
  return {
    'message': {
      'token':'dFNFuOlaRu2hq9PO6k8M5e:APA91bHce0Jn7VAp7AtWzNuqgfKEVvwK1U819RLrTS6QOkQvv32go3agi-9zahTp-zUy0d50KqTGoWN-JasrAVi4-txNW4d_3PEqbVlKRYuHmrgJ3Ag1K8NslKfmRpFByaFWQgrOxpwZ',
      'notification': {
        'title': 'betty Notification aandroid',
        'body': 'Notification from FCM'
      }
    }
  }

def _build_override_message():
  """Construct common notification message with overrides.

  Constructs a JSON object that will be used to customize
  the messages that are sent to iOS and Android devices.
  """
  fcm_message = _build_common_message()

  apns_override = {
    'payload': {
      'aps': {
        'badge': 1
      }
    },
    'headers': {
      'apns-priority': '10'
    }
  }

  android_override = {
    'notification': {
      'click_action': 'android.intent.action.MAIN'
    }
  }

  fcm_message['message']['android'] = android_override
  fcm_message['message']['apns'] = apns_override

  return fcm_message

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--message')
  args = parser.parse_args()
  if args.message and args.message == 'common-message':
    common_message = _build_common_message()
    print('FCM request body for message using common notification object:')
    print(json.dumps(common_message, indent=2))
    _send_fcm_message(common_message)
  elif args.message and args.message == 'override-message':
    override_message = _build_override_message()
    print('FCM request body for override message:')
    print(json.dumps(override_message, indent=2))
    _send_fcm_message(override_message)
  else:
    print('''Invalid command. Please use one of the following commands:
python messaging.py --message=common-message
python messaging.py --message=override-message''')

if __name__ == '__main__':
  main()