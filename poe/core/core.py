import requests

import browser_cookie3  # todo: check this lib and look for alternatives


def get_character_data(character_name, cookies=None):
    """
    Get character data from server.
    You can access ONLY your character.
    And also you need to be logged in 'www.pathofexile.com'

    :param character_name: Character name which data you want to receive
    :param cookies:
    :return: Data in json format
    """
    character_data_url = f'https://www.pathofexile.com/character-window/get-items?character={character_name}'

    if cookies is None:
        # Get cookies from all browsers
        cookies = browser_cookie3.load()

    return requests.get(character_data_url, cookies=cookies).json()


def get_equipped_gems_requirements(data):
    """
    Parse character data and return info about equipped gems and their requirements

    :param data: Character data in json
    :return: List of dicts with gem info
    """
    gems = []

    for item in data['items']:
        try:
            item['socketedItems']
        except KeyError:
            continue

        for gem in item['socketedItems']:
            requirements = []
            for req in gem['requirements']:
                if req['name'] in ('Dex', 'Int', 'Str'):
                    requirements.append((req['name'], req['values'][0][0]))

            gems.append({'name': gem['typeLine'], 'item': item['inventoryId'], 'requirements': requirements})

    return gems
