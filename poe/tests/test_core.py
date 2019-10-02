import pytest

from poe.core import core


class TestGetCharacterData:
    account_name = 'Skrierz'
    realm = 'pc'
    character_name = 'Skrierz_test'

    def test_returns_valid_data(self):
        data = core.get_character_data(self.account_name, self.realm, self.character_name)

        assert data['character']['name'] == self.character_name

    def test_returns_valid_gems(self):
        data = core.get_character_data(self.account_name, self.realm, self.character_name)

        gems = []
        for item in data['items']:
            try:
                item['socketedItems']
            except KeyError:
                continue

            gems.extend([i['typeLine'] for i in item['socketedItems']])
        assert [x['name'] for x in core.get_equipped_gems_requirements(data)] == gems

