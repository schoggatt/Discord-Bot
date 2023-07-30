import json

def get_config():
    with open('config.json') as f:
        return json.load(f)
    
def get_discord_token():
    return get_config()['discord_token']

def get_open_ai_token():
    return get_config()['open_ai_token']

def get_spotify_secret():
    return get_config()['spotify_secret']

def get_spotify_client():
    return get_config()['spotify_client']
