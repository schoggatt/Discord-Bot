import random
import requests


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == '!waifu --tags':
        return get_waifu_tags()

    if p_message.startswith('!waifu'):
        return get_waifu_payload(p_message)
    
    if p_message == '!help':
        return "`This is a help message that you can modify.`"
    
def get_waifu_payload(message):
    tags = message.split(' --')[1:]
    content_tags = list(filter(lambda t: t != 'nsfw', tags))
    url = 'https://api.waifu.im/search'
    params = {
        'included_tags': content_tags if len(content_tags) > 0  else ['waifu'],
        'is_nsfw': 'true' if 'nsfw' in tags else 'false',
        'height': '>=2000'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        image_url = data['images'][0]['url']
        return image_url
    else:
        print('Request failed with status code:', response.status_code)

def get_waifu_tags():
    url = 'https://api.waifu.im/tags'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tags = data['tags']
        return tags
        # Process the response data as needed
    else:
        print('Request failed with status code:', response.status_code)