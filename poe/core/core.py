from typing import List

import requests

import browser_cookie3  # todo: check this lib and look for alternatives


def get_character_data(account_name: str, realm: str, character_name: str) -> dict:
    """
    Get character data from server.

    :param realm: Account's realm: ('pc', 'ps4'(?), 'xbox'(?))
    :param account_name: Character owner account's name
    :param character_name: Character's name which data you want to receive
    :return: Character data
    """
    character_data_url = (f'https://www.pathofexile.com/character-window/get-items?accountName={account_name}'
                          f'&realm={realm}&character={character_name}')

    return requests.get(character_data_url).json()


def get_equipped_gems_requirements(data: dict) -> List[dict]:
    """
    Parse character data and return info about equipped gems and their requirements

    :param data: Character data
    :return: Gem's info
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
