import requests
import json

class ZohoMailService:
    def __init__(self, client_id, client_secret, refresh_token, zoho_refresh_folder, redirect_url, inboxfolder_id, sentfolder_id, startpageinbox, startpagesent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.zoho_refresh_folder = zoho_refresh_folder
        self.redirect_url = redirect_url
        self.startpageinbox = startpageinbox
        self.startpagesent = startpagesent
        self.inboxfolder_id = inboxfolder_id
        self.sentfolder_id = sentfolder_id
        self.base_url = 'https://mail.zoho.com/api/accounts'
        self.access_token = self.get_access_token()
        self.access_folder_token = self.get_access_token_folder()

    def get_access_token(self):
        url = "https://accounts.zoho.com/oauth/v2/token"
        payload = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri':self.redirect_url,
            'grant_type': 'refresh_token'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']
    
    def get_access_token_folder(self):
        url = "https://accounts.zoho.com/oauth/v2/token"
        payload = {
            'refresh_token': self.zoho_refresh_folder,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri':self.redirect_url,
            'grant_type': 'refresh_token'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']

    def get_inbox_emails(self, account_id):
        url = f'{self.base_url}/{account_id}/messages/view?folderId={self.inboxfolder_id}&start={self.startpageinbox}&limit=20'
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    

    def get_sent_emails(self, account_id):
        url = f'{self.base_url}/{account_id}/messages/view?folderId={self.sentfolder_id}&start={self.startpagesent}&limit=50'
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_folder(self, account_id):
        url = f'{self.base_url}/{account_id}/folders'
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_folder_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_email_content(self, account_id, folder_id, message_id):
        url = f'{self.base_url}/{account_id}/folders/{folder_id}/messages/{message_id}/content'
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        return response.json()


      #  https://mail.zoho.com/api/accounts/1761361000000008002/messages/1717139482527110001
# flutter: 1000.7f82d992344b9222a746be94d8050339.e326425f79aa39b073687e9f3a31e420
# flutter: {"fromAddress":"info@zugan.et","toAddress":"infozufan@gmail.com","subject":"Re: Testing email","content":"gggg","askReceipt":"yes","action":"reply"}

