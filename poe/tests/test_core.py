# -*- coding: utf-8 -*-

import time

import pytest

from poe.core import core
from poe.core.exceptions import ResourceNotFound


class TestCharacter:
    """Tests for Character class."""

    test_data = {
        'items': [
            {'league': 'Hardcore', 'name': '', 'typeLine': 'Wool Shoes', 'inventoryId': 'Boots', 'socketedItems': []},
            {
                'sockets': [{'group': 0, 'attr': 'S', 'sColour': 'R'}, {'group': 0, 'attr': 'S', 'sColour': 'R'}],
                'name': '',
                'typeLine': 'Superior Rusted Sword',
                'properties': [{'name': 'One Handed Sword', 'values': []}],
                'requirements': [{'name': 'Level', 'values': [['4', 0]]}],
                'inventoryId': 'Offhand',
                'socketedItems': [
                    {
                        'ilvl': 0,
                        'support': False,
                        'name': '',
                        'typeLine': 'Cleave',
                        'properties': [
                            {'name': 'Attack, AoE, Physical, Melee', 'values': [], 'displayMode': 0},
                            {'name': 'Level', 'values': [['3', 0]]},
                        ],
                        'additionalProperties': [
                            {
                                'name': 'Experience',
                                'values': [['1/1554', 0]],
                                'progress': 0.000643500650767237,
                                'type': 20,
                            },
                        ],
                        'requirements': [{'name': 'Level', 'values': [['4', 0]]}],
                        'socket': 0,
                        'colour': 'S',
                    },
                    {
                        'ilvl': 0,
                        'support': False,
                        'name': '',
                        'typeLine': 'Cleave',
                        'properties': [
                            {'name': 'Attack, AoE, Physical, Melee', 'values': [], 'displayMode': 0},
                            {'name': 'Level', 'values': [['2', 0]], 'displayMode': 0, 'type': 5},
                            {'name': 'Mana Cost', 'values': [['6', 0]], 'displayMode': 0},
                            {'name': 'Attack Speed', 'values': [['80% of base', 0]], 'displayMode': 0},
                            {'name': 'Effectiveness of Added Damage', 'values': [['127%', 0]], 'displayMode': 0},
                        ],
                        'additionalProperties': [
                            {
                                'name': 'Experience',
                                'values': [['161/308', 0]],
                                'progress': 0.5227272510528564,
                                'type': 20,
                            },
                        ],
                        'requirements': [{'name': 'Level', 'values': [['2', 0]], 'displayMode': 0}],
                        'socket': 1,
                        'colour': 'S',
                    },
                ],
            },
            {'name': '', 'typeLine': 'Iron Ring'},
            {'typeLine': 'Quicksilver Flask'},
        ],
        'character': {
            'name': 'Skrierz_test',
            'league': 'Hardcore',
            'classId': 4,
            'ascendancyClass': 0,
            'class': 'Duelist',
            'level': 4,
            'experience': 4641,
        },
    }
    expected_parsed_values = [
        {'name': 'Cleave', 'equipped_in': 'Offhand', 'requirements': []},
        {'name': 'Cleave', 'equipped_in': 'Offhand', 'requirements': []},
    ]

    def test_class_correct_parse_data(self):
        """Test that parsing algorithm works correctly."""
        character = core.Character(self.test_data)
        assert character.get_gems_info() == self.expected_parsed_values


class TestPOERequests:
    """Tests server requests."""

    # Character for tests
    account_name = 'Skrierz'
    realm = 'pc'
    character_name = 'Skrierz_test'
    invalid_name = 'NonExistentName'

    def teardown(self):
        """Tests setup."""
        # Prevent too many requests to POE server
        time.sleep(1)

    def test_returns_valid_data(self):
        """Test that valid request returns valid character data."""
        request = core.CharacterDataRequests(self.account_name, self.realm, self.character_name)
        data = request.get_character_items()

        assert data['character']['name'] == self.character_name

    @pytest.mark.parametrize(
        'invalid_data',
        [
            (invalid_name, realm, character_name),
            (account_name, invalid_name, character_name),
            (account_name, realm, invalid_name),
        ],
    )
    def test_invalid_character_credentials(self, invalid_data):
        """Test that invalid request returns invalid character data."""
        request = core.CharacterDataRequests(*invalid_data)

        with pytest.raises(ResourceNotFound):
            request.get_character_items()
