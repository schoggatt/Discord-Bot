from requests import post
import base64
import json

from config import get_spotify_client, get_spotify_secret

client_id = get_spotify_client()
client_secret = get_spotify_secret()

def get_spotify_token():
    auth_string = client_id + ':' + client_secret
    auth_string_bytes = auth_string.encode('utf-8')
    auth_base64_bytes = str(base64.b64encode(auth_string_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Authorization': 'Basic ' + auth_base64_bytes,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token
    