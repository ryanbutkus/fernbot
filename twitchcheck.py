#!/usr/bin/python3
import fern_keys
import requests
import os

client_id = fern_keys.twitch_client_id
client_secret = fern_keys.twitch_client_secret
streamer = 'princess_jem4'

# OAuth token URL and data
url = 'https://id.twitch.tv/oauth2/token'
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

get_token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

access_token_response = requests.post(url, data=payload, headers=get_token_headers)
# Parse the response
if access_token_response.status_code == 200:
    access_token = access_token_response.json().get('access_token')

get_status_headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

url = f'https://api.twitch.tv/helix/streams?user_login={streamer}'
response = requests.get(url, headers=get_status_headers)
data = response.json()

if data['data']:
    if not os.path.isfile("/home/ubuntu/repos/fernbot/" + streamer):
        with open("/home/ubuntu/repos/fernbot/" + streamer, 'w') as file:
           file.write("/home/ubuntu/repos/fernbot/" + streamer)
else:
    if os.path.isfile("/home/ubuntu/repos/fernbot/" + streamer):
        os.remove("/home/ubuntu/repos/fernbot/" + streamer)
