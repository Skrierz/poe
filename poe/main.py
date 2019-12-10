# -*- coding: utf-8 -*-

from poe.core import core
from poe.core.exceptions import ResourceNotFound, ForbiddenRequest


def request_character_credentials_from_user():
    return (
        input('Введите имя Вашего аккаунта: '),
        input('Введите имя Вашего персонажа: '),
    )


def calculate_character_stats(class_id, passives):
    base_stats = core.GameInfo().get_base_character_stats(str(class_id))
    char_passives = core.CharacterPassives(passives)
    passives_add_stats = char_passives.get_add_stats_from_passives()

    return {
        'int': base_stats['base_int'] + passives_add_stats['int'],
        'str': base_stats['base_str'] + passives_add_stats['str'],
        'dex': base_stats['base_dex'] + passives_add_stats['dex'],
    }


def main():
    request = None
    character_data = {}
    character_found = False

    while not character_found:
        character_credentials = request_character_credentials_from_user()
        request = core.CharacterDataRequests(*character_credentials)
        try:
            character_data = request.get_items()
        except (ResourceNotFound, ForbiddenRequest) as e:
            print(e)
        else:
            character_found = True

    character = core.Character(character_data)
    gems = character.get_gems_info()
    [print(f'gem: {x["name"]}. requirements: {x["requirements"]}') for x in gems]

    current_stats = calculate_character_stats(
        character.get_class_id(),
        request.get_passives(),
    )
    print(f'Character stats without equipped items: {current_stats}')

    input('Press Enter to close app...')


if __name__ == '__main__':
    main()
