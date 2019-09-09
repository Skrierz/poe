import requests
import json


with open('response.txt', 'r') as fp:
    data = json.load(fp)


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
