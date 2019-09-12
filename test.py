import requests
import json
import browser_cookie3 # todo: check this lib and look for alternatives


def get_character_data(character_name):
    '''
    Get character data from server.
    You can access ONLY your character.
    And also you need to be logged in 'www.pathofexile.com'

    :param character_name: Character name which data you want to receive
    :return: Data in json format
    '''
    character_data_url = f'https://www.pathofexile.com/character-window/get-items?character={character_name}'

    # Get cookies from all browsers
    cj = browser_cookie3.load()

    return requests.get(character_data_url, cookies=cj).json()


def get_equipped_gems_requirements(data):
    '''
    Parse character data and return info about equipped gems and their requirements

    :param data: Character data in json
    :return: Dict with key = gem name and value = list of tuples, where: 1st item - stat name; 2nd item - needed value
    '''
    gems = {}

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
            gems[gem["typeLine"]] = requirements

    return gems


def main():
    CHARACTER = 'BlyatLiga'
    gems = get_equipped_gems_requirements(get_character_data(CHARACTER))
    [print(f'gem: {k}. requirements: {v}') for k,v in gems.items()]


if __name__ == '__main__':
    main()
