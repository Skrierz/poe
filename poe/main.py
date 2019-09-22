from poe.core.core import get_character_data, get_equipped_gems_requirements


def main():
    character_name = input('Введите имя Вашего персонажа: ')

    gems = get_equipped_gems_requirements(get_character_data(character_name))
    [print(f'gem: {x[0]}. requirements: {x[1]}') for _, v in gems.items() for x in v]


if __name__ == '__main__':
    main()
