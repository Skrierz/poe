from poe.core.core import get_character_data, get_equipped_gems_requirements


def main():
    character_name = input('Введите имя Вашего персонажа: ')

    gems = get_equipped_gems_requirements(get_character_data(character_name))
    [print(f'gem: {k}. requirements: {v}') for k, v in gems.items()]


if __name__ == '__main__':
    main()
