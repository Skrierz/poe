from poe.core.core import get_character_data, get_equipped_gems_requirements
from poe.core.exceptions import ResourceNotFoundException


def request_character_credentials_from_user():
    return input('Введите имя Вашего аккаунта: '), \
           input('Введите ваш реалм ("pc", "ps4"(?), "xbox"(?)): '),\
           input('Введите имя Вашего персонажа: ')


def main():
    character_credentials = request_character_credentials_from_user()

    character_data = {}
    character_found = False
    while not character_found:
        try:
            character_data = get_character_data(*character_credentials)
        except ResourceNotFoundException as e:
            print(e)
            character_credentials = request_character_credentials_from_user()
        else:
            character_found = True

    gems = get_equipped_gems_requirements(character_data)
    [print(f'gem: {x["name"]}. requirements: {x["requirements"]}') for x in gems]

    input('Press Enter to close app...')


if __name__ == '__main__':
    main()
