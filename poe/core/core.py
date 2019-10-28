# -*- coding: utf-8 -*-

from typing import List, Any, Dict  # noqa: Strange error while all seems correct I001

import requests

from poe.core.exceptions import ResourceNotFoundException


def get_character_data(
    account_name: str,
    realm: str,
    character_name: str,
) -> dict:
    """Get character data from server.

    :param realm: Account's realm: ('pc', 'ps4'(?), 'xbox'(?))
    :param account_name: Character owner account's name
    :param character_name: Character's name which data you want to receive
    :return: Character data
    """
    base_url = 'https://www.pathofexile.com/character-window/get-items'
    request_params = {
        'accountName': account_name,
        'realm': realm,
        'character': character_name,
    }

    character_data = requests.get(base_url, params=request_params).json()

    if 'error' in character_data:
        raise ResourceNotFoundException()

    return character_data


class Character:
    """Class with character data."""

    def __init__(self, character_data: Dict[str, Any]) -> None:
        """Initialize character class.

        :param character_data: Character data from game server
        """
        self._raw_data = character_data
        self._equipped_gems = []
        self._parse_equipped_gems()

    def get_gems_info(self) -> List[dict]:
        """Return equipped gems."""
        return self._equipped_gems

    def _parse_equipped_gems(self) -> None:
        """Parse gems info from character data."""
        for item in self._raw_data['items']:  # noqa: It's item WPS110
            if item.get('socketedItems') is None:
                continue

            for gem in item['socketedItems']:
                gem_data = {
                    'name': gem['typeLine'],
                    'equipped_in': item['inventoryId'],
                    'requirements': self._parse_gem_requirements(gem),
                }

                self._equipped_gems.append(gem_data)

    # noinspection PyMethodMayBeStatic
    def _parse_gem_requirements(self, gem_data: dict) -> List[tuple]:
        """Parse gem requirements from gem data.

        :param gem_data: Gem's data from equipped item
        :return: Gem's requirements
        """
        requirements = []
        for req in gem_data['requirements']:
            if req['name'] in {'Dex', 'Int', 'Str'}:
                gem_requirement = (req['name'], req['values'][0][0])
                requirements.append(gem_requirement)

        return requirements
