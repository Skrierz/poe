# -*- coding: utf-8 -*-

from typing import List, Any, Dict  # noqa: Strange error while all seems correct I001
from pathlib import Path
import json

import requests

from poe.core.exceptions import server_error_router


class CharacterDataRequests:
    """Class for requesting data from server."""

    def __init__(
            self,
            account_name: str,
            realm: str,
            character_name: str
    ) -> None:
        """Initializer.

        :param account_name: Character owner account's name
        :param realm: Account's realm: ('pc', 'ps4'(?), 'xbox'(?))
        :param character_name: Character's name which data you want to receive
        """
        self._base_url = 'https://www.pathofexile.com/character-window/'
        self._account_name = account_name
        self._realm = realm
        self._character_name = character_name

    def get_items(self) -> Dict[str, Any]:
        """Request character items from server.

        :return: Character items
        """
        server_method = 'get-items'
        request_params = {
            'accountName': self._account_name,
            'realm': self._realm,
            'character': self._character_name,
        }
        return self._make_request(server_method, request_params)

    def get_passives(self) -> Dict[str, Any]:
        """Request character passives from server.

        :return: Character passives
        """
        server_method = 'get-passive-skills'
        request_params = {
            'accountName': self._account_name,
            'realm': self._realm,
            'character': self._character_name,
        }
        return self._make_request(server_method, request_params)

    def _check_error(self, response: Dict[str, Any]) -> None:
        """Check errors in response.

        :param response: Response from server
        """
        if 'error' in response:
            raise server_error_router(response['error'])

    def _make_request(
            self,
            method: str,
            params: dict
    ) -> Dict[str, Any]:
        """Method to make request to server.

        :param method: Server method
        :param params: Parameters for request
        :return: Server response if success or raise Exception
        """
        response = requests.get(self._base_url + method, params=params).json()
        self._check_error(response)

        return response


class Character:
    """Class with character data."""

    def __init__(self, character_data: Dict[str, Any]) -> None:
        """Initialize character class.

        :param character_data: Character data from game server
        """
        self._raw_data = character_data
        self._equipped_gems = []

    def get_gems_info(self) -> List[dict]:
        """Return equipped gems."""
        if not self._equipped_gems:
            self._parse_equipped_gems()
        return self._equipped_gems

    def get_class_id(self) -> str:
        """Get character class id."""
        return self._raw_data['character']['classId']

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


class GameInfo:
    """Borg class to game data read from data/passives file."""
    __shared_state = {}

    def __init__(self, path_to_game_data: str = None) -> None:
        """Read data from file if not read before.

        :param path_to_game_data: Relative path to file with game data
        """
        self.__dict__ = self.__shared_state
        if not path_to_game_data:
            path_to_game_data = '../data/passives.bbl'

        core_dir = Path(__file__).parent.resolve()
        game_info_relative_path = Path(path_to_game_data)
        game_info_path = core_dir.joinpath(game_info_relative_path).resolve()

        try:
            self._game_info
        except AttributeError:
            with open(game_info_path, 'r') as fp:
                self._game_info = json.load(fp)

    def get_passives(self, passive_ids: List[str]) -> dict:
        """Resolve passive ids to passives data.

        :param passive_ids: Ids of passives data to get
        :return: Passives data
        """
        return {x: self._game_info['nodes'][x] for x in passive_ids}

    def get_base_character_stats(self, class_id: str) -> Dict[str, Any]:
        """Resolve class id to class base stats.

        :param class_id: Id of class data to get
        :return: Class data
        """
        return self._game_info['characterData'][class_id]


class CharacterPassives:
    """Class with info about character passives."""

    def __init__(self, passives_data: Dict[str, Any]) -> None:
        """Initialize class.

        :param passives_data: Passives got from server
        """
        self._raw_passives = passives_data
        self._character_passives = {}

    def get_add_stats_from_passives(self) -> dict:
        """Parse added stats from passives.

        :return: Added character stats
        """
        # Fill self._character_passives if empty
        self.get_passive(None)

        add_stats = {'int': 0, 'str': 0, 'dex': 0}

        for passive in self._character_passives.values():
            add_stats['int'] += passive['ia']
            add_stats['str'] += passive['sa']
            add_stats['dex'] += passive['da']

        return add_stats

    def get_passive(self, passive_id: str) -> Dict[str, Any]:
        """Get character passive data.

        :param passive_id: Character passive id
        :return: Passive data
        """
        if not self._character_passives:
            self._update_character_passives()
        return self._character_passives.get(passive_id)

    def _update_raw_data(self, passives_data: Dict[str, Any]) -> None:
        """Update character passives data.

        :param passives_data: Passives got from server
        """
        self._raw_passives = passives_data
        self._character_passives = {}

    def _update_character_passives(self) -> None:
        """Get passives data from GameInfo class."""
        # From server passives returns as int
        passives = [str(x) for x in self._raw_passives['hashes']]

        self._character_passives = GameInfo().get_passives(passives)
