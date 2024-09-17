from django.shortcuts import render
from .zoho_email import ZohoMailService
from .models import ZohoMailAccount, new_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# emailapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def zoho_mail_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get('subject')
            from_address = data.get('from')

            # Process the email information here
            print(f"New Email - Subject: {subject}, From: {from_address},")
            new_email.objects.create(subject = subject, fromm = from_address, body = data)
            zoho_account = get_object_or_404(ZohoMailAccount, pk=1)
            zoho_account.email = 'true'
            zoho_account.save()


            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "method not allowed"}, status=405)




@api_view(['GET'])
def get_email_parameters(request):
    zoho_account = get_object_or_404(ZohoMailAccount, pk=1)

    data = {
        'accountid':zoho_account.account_id,
        'email':zoho_account.zoho_email,
        'client_id': zoho_account.client_id,
        'client_secret': zoho_account.client_secr,
        'refresh_token': zoho_account.zoho_refresh_token,
        'zoho_refresh_folder': zoho_account.zoho_refresh_folder,
        'redirect_url': zoho_account.redirect_uri,
        'inboxfolder_id':zoho_account.inbox_folder_id,
        'sentfolder_id': zoho_account.sent_folder_id,
        'startpageinbox': 1,
        'startpagesent': 1,
        'update':zoho_account.email
    }

    print(data)
    zoho_account.email = 'true'
    zoho_account.save()
    return Response(data, status=status.HTTP_200_OK)

def list_inbox_emails(request):
    user = request.user
    zoho_account = ZohoMailAccount.objects.get(user=user)
    client_id = zoho_account.client_id
    client_secret = zoho_account.client_secr 
    refresh_token = zoho_account.zoho_refresh_token
    zoho_refresh_folder1 = zoho_account.zoho_refresh_folder
    redirect_url = zoho_account.redirect_uri
    sentfolder_id = zoho_account.sent_folder_id
    inboxfolder_id = zoho_account.inbox_folder_id

    zoho_service = ZohoMailService(client_id, client_secret, refresh_token, zoho_refresh_folder1, redirect_url, inboxfolder_id, sentfolder_id, 1, 1)
    account_id = zoho_account.account_id
    sent = zoho_service.get_sent_emails(account_id)
    inbox = zoho_service.get_inbox_emails(account_id)

    return render(request, 'inbox.html', {'emails': inbox['data'], 'sent':sent['data']})


def get_email_content(request, folder_id, message_id):
    zoho_account = get_object_or_404(ZohoMailAccount, pk=1)
    client_id = zoho_account.client_id
    client_secret = zoho_account.client_secr 
    refresh_token = zoho_account.zoho_refresh_token
    zoho_refresh_folder = zoho_account.zoho_refresh_folder
    redirect_url = zoho_account.redirect_uri
    inbox_folder_id = zoho_account.inbox_folder_id
    sent_folder_id = zoho_account.sent_folder_id
    account_id = zoho_account.account_id
    zoho_service = ZohoMailService(client_id, client_secret, refresh_token, zoho_refresh_folder, redirect_url, inbox_folder_id, sent_folder_id, 1, 1)

    inbox_emails = zoho_service.get_email_content(account_id, folder_id, message_id)
    return JsonResponse(inbox_emails)

def list_emails(request):
    zoho_account = get_object_or_404(ZohoMailAccount, pk=1)
    client_id = zoho_account.client_id
    client_secret = zoho_account.client_secr 
    refresh_token = zoho_account.zoho_refresh_token
    zoho_refresh_folder = zoho_account.zoho_refresh_folder
    redirect_url = zoho_account.redirect_uri
    inbox_folder_id = zoho_account.inbox_folder_id
    sent_folder_id = zoho_account.sent_folder_id

    zoho_service = ZohoMailService(client_id, client_secret, refresh_token, zoho_refresh_folder, redirect_url, inbox_folder_id, sent_folder_id, 1, 1)
    account_id = zoho_account.account_id

    inbox_emails = zoho_service.get_inbox_emails(account_id)
    sent_emails = zoho_service.get_sent_emails(account_id)
    print(inbox_emails)

    return JsonResponse({'inbox_emails': inbox_emails['data'], 'sent_emails': sent_emails['data']})
'''
#http://127.0.0.1:8090/?state=testing&
#code=1000.20f61a04ebc625c0629797102cf3c2a7.3a0ea06890c770f5a17f0bebbf48d6f9
#&location=us&accounts-server=https%3A%2F%2Faccounts.zoho.com&


request to get code https://accounts.zoho.com/oauth/v2/auth?response_type=code&client_id=1000.X7QKPWVBWTMPZXX052742CWHO8PT0B&scope=ZohoMail.folders.ALL&redirect_uri=http://127.0.0.1:8090&state=testing&access_type=offline

result http://127.0.0.1:8090/?state=testing&code=
1000.b3a746c41bbe3382c7307ae090b18f3e.794d03016f3317ce33a7bbeacb5a6151
&location=us&accounts-server=https%3A%2F%2Faccounts.zoho.com&

 requst to get accesid https://accounts.zoho.com/oauth/v2/token?code=1000.c05e3a767a1311224511ee13f097e179.dc24d302c9c9311646bc3a3f80163cfa&grant_type=authorization_code&client_id=1000.X7QKPWVBWTMPZXX052742CWHO8PT0B&client_secret=7296dca99581aaac8f9d4427755c1f05b88e0bf1f0&redirect_uri=127.0.0.1:8090&scope=ZohoMail.accounts.READ

{'access_token': '1000.2c4c4f677e2c5502c9cc86750613a9d9.a43a68cd3a815088d8a8a11193f8743d', 
'scope': 'ZohoMail.accounts.READ', 
'api_domain': 'https://www.zohoapis.com',
 'token_type': 'Bearer',
   'expires_in': 3600}



   {'access_token': '1000.ee6ef8af716223aa8a28c7fd9b7812dd.215db50f9f3eaad680da27e3f7781205', 
   'refresh_token': '1000.59a6d5406cb574075d5dcac773cd5638.0167104b6a62a95feebf9af4046b790a', 'scope': 'ZohoMail.messages.ALL', 'api_domain': 'https://www.zohoapis.com', 'token_type': 'Bearer', 'expires_in': 3600}






   {
    "status": {
        "code": 200,
        "description": "success"
    },
    "data": [{
        "country": "et",
        "lastLogin": 1716820111249,
        "mxStatus": true,
        "activeSyncEnabled": false,
        "incomingBlocked": false,
        "language": "en",
        "type": "ZOHO_ACCOUNT",
        "extraStorage": {},
        "incomingUserName": "info@zufan.et",
        "emailAddress": [{
            "isAlias": false,
            "isPrimary": true,
            "mailId": "info@zufan.et",
            "isConfirmed": true
        }, {
            "isAlias": false,
            "isPrimary": false,
            "mailId": "robelt59@gmail.com",
            "isConfirmed": true
        }],
        "mailboxStatus": "enabled",
        "popBlocked": false,
        "usedStorage": 7045,
        "spamcheckEnabled": true,
        "imapAccessEnabled": false,
        "timeZone": "Africa/Addis_Ababa",
        "accountCreationTime": 1677629154893,
        "zuid": 804339409,
        "webBlocked": false,
        "planStorage": 5,
        "firstName": "Robel",
        "accountId": "1761361000000008002",
        "sequence": 1,
        "mailboxAddress": "info@zufan.et",
        "lastPasswordReset": 1677629156028,
        "tfaEnabled": false,
        "iamStatus": 1,
        "status": true,
        "lastName": "Tsegaye",
        "accountDisplayName": "info",
        "role": "super_admin",
        "gender": "MALE",
        "accountName": "zufan",
        "displayName": "robel",
        "isLogoExist": true,
        "URI": "https://mail.zoho.com/api/accounts/1761361000000008002",
        "primaryEmailAddress": "info@zufan.et",
        "enabled": true,
        "mailboxCreationTime": 1707395125502,
        "basicStorage": "free",
        "lastClient": "WEB_ZM",
        "allowedStorage": 5242880,
        "sendMailDetails": [{
            "sendMailId": "1761361000000008004",
            "displayName": "robel",
            "serverName": "smtpout.mail.zoho.com",
            "signatureId": "1761361000000010003",
            "serverPort": 25,
            "userName": "info@zufan.et",
            "connectionType": "plain",
            "mode": "mailbox",
            "validated": false,
            "fromAddress": "info@zufan.et",
            "smtpConnection": 0,
            "validationRequired": true,
            "validationState": 0,
            "status": true
        }],
        "popFetchTime": -1,
        "address": {},
        "planType": 0,
        "userExpiry": -1,
        "popAccessEnabled": false,
        "imapBlocked": false,
        "iamUserRole": "super_admin",
        "outgoingBlocked": false,
        "policyId": {
            "zoid": 804335360,
            "1082700000237795691": "Business Policy"
        },
        "smtpStatus": true,
        "extraEDiscoveryStorage": {}
    }]
}

'''