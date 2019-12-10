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

    def test_get_gems_info_correct_data(self):
        """Gems parsing algorithm works correctly."""
        expected_parsed_values = [
            {'name': 'Cleave', 'equipped_in': 'Offhand', 'requirements': []},
            {'name': 'Cleave', 'equipped_in': 'Offhand', 'requirements': []},
        ]

        character = core.Character(self.test_data)
        assert character.get_gems_info() == expected_parsed_values

    def test_get_class_id_correct_data(self):
        """Class id parsed correctly."""
        expected_class_id = 4

        character = core.Character(self.test_data)
        assert character.get_class_id() == expected_class_id


class TestCharacterDataRequests:
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

    def test_get_items_returns_valid_data(self):
        """Valid request returns valid character data."""
        request = core.CharacterDataRequests(self.account_name, self.character_name, self.realm)
        data = request.get_items()

        assert data['character']['name'] == self.character_name

    @pytest.mark.parametrize(
        'invalid_data',
        [
            (invalid_name, character_name, realm),
            (account_name, invalid_name, realm),
            (account_name, character_name, invalid_name),
        ],
    )
    @pytest.mark.parametrize('method_name', ['get_items', 'get_passives'])
    def test_invalid_character_credentials(self, invalid_data, method_name):
        """Invalid request returns invalid character data."""
        request = core.CharacterDataRequests(*invalid_data)
        cls_method = getattr(request, method_name)

        with pytest.raises(ResourceNotFound):
            cls_method()

    def test_get_passives_returns_valid_data(self):
        """Parse algorithm for passives works correctly."""
        expected_hashes_in_passives = [476, 24377, 30691, 39725, 40867, 42911, 47389, 56803, 63649]

        request = core.CharacterDataRequests(self.account_name, self.character_name, self.realm)
        data = request.get_passives()
        assert all([x in data.get('hashes') for x in expected_hashes_in_passives])


class TestGameInfo:
    """Tests GameInfo class."""

    def test_get_passives_returns_valid_data(self):
        """get_passives returns passives data for correct ids."""
        passive_ids = ['476', '24377']
        expected_answer = {
            '476': {
                'id': 476,
                'icon': 'Art/2DArt/SkillIcons/passives/plusstrength.png',
                'ks': False,
                'not': False,
                'dn': 'Strength',
                'm': False,
                'isJewelSocket': False,
                'isMultipleChoice': False,
                'isMultipleChoiceOption': False,
                'passivePointsGranted': 0,
                'spc': [],
                'sd': ['+10 to Strength'],
                'g': 408,
                'o': 0,
                'oidx': 0,
                'sa': 10,
                'da': 0,
                'ia': 0,
                'out': [],
                'in': [476, 476, 476, 476]
            },
            '24377': {
                'id': 24377,
                'icon': 'Art/2DArt/SkillIcons/passives/attackspeed.png',
                'ks': False,
                'not': False,
                'dn': 'Attack Speed',
                'm': False,
                'isJewelSocket': False,
                'isMultipleChoice': False,
                'isMultipleChoiceOption': False,
                'passivePointsGranted': 0,
                'spc': [],
                'sd': ['3% increased Attack Speed'],
                'g': 227,
                'o': 2,
                'oidx': 11,
                'sa': 0,
                'da': 0,
                'ia': 0,
                'out': [35568, 56803],
                'in': [24377]
            },
        }

        passive = core.GameInfo().get_passives(passive_ids)
        assert passive == expected_answer

    def test_get_base_character_stats_return_valid_data(self):
        """get_base_character returns base stats for correct class id."""
        class_id = '4'
        expected_answer = {'base_str': 23, 'base_dex': 23, 'base_int': 14}

        character_base_stats = core.GameInfo().get_base_character_stats(class_id)
        assert character_base_stats == expected_answer


class TestCharacterPassives:
    """Tests for CharacterPassives class."""

    @pytest.mark.parametrize(
        'passive_ids, expected_result',
        [
            ({'hashes': [24377]}, {'int': 0, 'str': 0, 'dex': 0}),
            ({'hashes': [30691]}, {'int': 10, 'str': 0, 'dex': 0}),
            ({'hashes': [476]}, {'int': 0, 'str': 10, 'dex': 0}),
            ({'hashes': [63649]}, {'int': 0, 'str': 0, 'dex': 10}),
            ({'hashes': [30691, 476]}, {'int': 10, 'str': 10, 'dex': 0}),
            ({'hashes': [30691, 63649]}, {'int': 10, 'str': 0, 'dex': 10}),
            ({'hashes': [476, 63649]}, {'int': 0, 'str': 10, 'dex': 10}),
            ({'hashes': [30691, 476, 63649]}, {'int': 10, 'str': 10, 'dex': 10}),
        ],
    )
    def test_get_add_stats_from_passives_parse_add_stats_correctly(self, passive_ids, expected_result):
        """Parse algorithm for added stats works correctly."""
        passives = core.CharacterPassives(passive_ids)
        assert passives.get_add_stats_from_passives() == expected_result

    @pytest.mark.parametrize(
        'passives, passive_id, expected_result',
        [
            ({'hashes': [61308]}, '61308', {'id': 61308, 'icon': 'Art/2DArt/SkillIcons/passives/amplify.png', 'ks': False, 'not': True, 'dn': 'Amplify', 'm': False, 'isJewelSocket': False, 'isMultipleChoice': False, 'isMultipleChoiceOption': False, 'passivePointsGranted': 0, 'spc': [], 'sd': ['10% increased Area of Effect', '20% increased Area Damage'], 'g': 142, 'o': 2, 'oidx': 11, 'sa': 0, 'da': 0, 'ia': 0, 'out': [], 'in': [61308, 61308, 61308]}),
            ({'hashes': [43303]}, '43303', {'id': 43303, 'icon': 'Art/2DArt/SkillIcons/passives/2handeddamage.png', 'ks': False, 'not': False, 'dn': 'Two Handed Melee Damage', 'm': False, 'isJewelSocket': False, 'isMultipleChoice': False, 'isMultipleChoiceOption': False, 'passivePointsGranted': 0, 'spc': [], 'sd': ['12% increased Physical Damage with Two Handed Melee Weapons', '12% increased Damage with Ailments from Attack Skills while wielding a Two Handed Weapon'], 'g': 226, 'o': 2, 'oidx': 5, 'sa': 0, 'da': 0, 'ia': 0, 'out': [30842, 34031], 'in': [43303]}),
            ({'hashes': [24377]}, '24377', {'id': 24377, 'icon': 'Art/2DArt/SkillIcons/passives/attackspeed.png', 'ks': False, 'not': False, 'dn': 'Attack Speed', 'm': False, 'isJewelSocket': False, 'isMultipleChoice': False, 'isMultipleChoiceOption': False, 'passivePointsGranted': 0, 'spc': [], 'sd': ['3% increased Attack Speed'], 'g': 227, 'o': 2, 'oidx': 11, 'sa': 0, 'da': 0, 'ia': 0, 'out': [35568, 56803], 'in': [24377]}),
        ],
    )
    def test_get_passive(self, passives, passive_id, expected_result):
        """get_passive returns valid data for passive id."""
        passives = core.CharacterPassives(passives)
        assert passives.get_passive(passive_id) == expected_result
