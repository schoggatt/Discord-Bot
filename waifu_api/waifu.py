import requests

# TODO: Need to figure out how to do tag prefixes for the function
def get_waifu_payload(message):
    tags = message
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
        tag_response = 'Here are the tags you can use...\n\n'
        tag_response += '**Tags**: \n'
        tag_response += '\t**NSFW**: \n'
        for tag in data['nsfw']:
            tag_response += f'\t\t-{tag}\n'
        tag_response += '\t**SFW**: \n'
        for tag in data['versatile']:
            tag_response += f'\t\t-{tag}\n'
        return tag_response
        # Process the response data as needed
    else:
        print('Request failed with status code:', response.status_code)