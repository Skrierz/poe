import pytest

from poe.core import core


class TestGetCharacterData:
    character_name = 'Skrierz'

    def test_returns_valid_data(self):
        data = core.get_character_data(self.character_name)


        assert data['character']['name'] == self.character_name
