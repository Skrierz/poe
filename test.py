import requests
import json
import browser_cookie3 # todo: check this lib and look for alternatives


def get_data():
    with open('response.txt', 'r') as fp:
        data = json.load(fp)


def get_equiped_gems_requiremens():
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
            print(f'gem: {gem["typeLine"]}. requiremens: {requirements}')


def test():
    cj = browser_cookie3.chrome()
    return requests.get('https://www.pathofexile.com', cookies=cj)


def main():
    print(test())


if __name__ == '__main__':
    main()
