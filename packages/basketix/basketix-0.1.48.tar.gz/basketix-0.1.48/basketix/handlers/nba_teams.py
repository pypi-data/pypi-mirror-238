"""NBA teams module"""

from ..exceptions import UnknownNBATeam


class NbaTeamsHandler:
    """Handle NBA teams."""

    _MAPPING_ID_TRICODE = {
        "1610612737": "ATL",
        "1610612738": "BOS",
        "1610612739": "CLE",
        "1610612740": "NOP",
        "1610612741": "CHI",
        "1610612742": "DAL",
        "1610612743": "DEN",
        "1610612744": "GSW",
        "1610612745": "HOU",
        "1610612746": "LAC",
        "1610612747": "LAL",
        "1610612748": "MIA",
        "1610612749": "MIL",
        "1610612750": "MIN",
        "1610612751": "BKN",
        "1610612752": "NYK",
        "1610612753": "ORL",
        "1610612754": "IND",
        "1610612755": "PHI",
        "1610612756": "PHX",
        "1610612757": "POR",
        "1610612758": "SAC",
        "1610612759": "SAS",
        "1610612760": "OKC",
        "1610612761": "TOR",
        "1610612762": "UTA",
        "1610612763": "MEM",
        "1610612764": "WAS",
        "1610612765": "DET",
        "1610612766": "CHA",
    }

    _MAPPING_TRICODE_ID = {tricode: team_id for team_id, tricode in _MAPPING_ID_TRICODE.items()}

    @classmethod
    def tricode(cls, team_id: str):
        """
        Returns tricode from an ID.

        Raises UnknownTeam error if team_id is unknown.
        """
        try:
            return cls._MAPPING_ID_TRICODE[team_id]
        except KeyError as err:
            raise UnknownNBATeam(team_id=team_id) from err

    @classmethod
    def id(cls, tricode: str):
        """
        Returns ID from a tricode.

        Raises UnknownTeam error if tricode is unknown.
        """
        try:
            return cls._MAPPING_TRICODE_ID[tricode.upper()]
        except KeyError as err:
            raise UnknownNBATeam(tricode=tricode.upper()) from err
