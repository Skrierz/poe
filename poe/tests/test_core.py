import time

import pytest

from poe.core import core
from poe.core.exceptions import ResourceNotFoundException


class TestCharacterData:
    account_name = 'Skrierz'
    realm = 'pc'
    character_name = 'Skrierz_test'
    invalid_name = 'NonexistentName'

    def teardown(self):
        """Tests setup"""

        # Prevent too many requests to POE server
        time.sleep(1)

    def test_returns_valid_data(self):
        data = core.get_character_data(self.account_name, self.realm, self.character_name)

        assert data['character']['name'] == self.character_name

    def test_returns_valid_gems(self):
        data = core.get_character_data(self.account_name, self.realm, self.character_name)
        character = core.Character(data)

        gems = []
        for item in data['items']:
            try:
                item['socketedItems']
            except KeyError:
                continue

            gems.extend([i['typeLine'] for i in item['socketedItems']])
        assert [x['name'] for x in character.get_gems_info()] == gems

    @pytest.mark.parametrize('invalid_data',
                             [(invalid_name, realm, character_name),
                              (account_name, invalid_name, character_name),
                              (account_name, realm, invalid_name)])
    def test_invalid_character_credentials(self, invalid_data):
        with pytest.raises(ResourceNotFoundException):
            core.get_character_data(*invalid_data)
