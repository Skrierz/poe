from poe.core.core import get_character_data, get_equipped_gems_requirements


def main():
    character_name = input('Введите имя Вашего персонажа: ')

    gems = get_equipped_gems_requirements(get_character_data(character_name))
    [print(f'gem: {x["name"]}. requirements: {x["requirements"]}') for x in gems]

    input('Press Enter to close app...')


if __name__ == '__main__':
    main()
