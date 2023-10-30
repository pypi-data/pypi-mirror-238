"""Unknown NBA team module"""

from typing import Optional


class UnknownNBATeam(Exception):
    """Unknown NBA team error"""

    def __init__(self, team_id: Optional[str] = None, tricode: Optional[str] = None) -> None:
        message = "Unknown NBA team."
        if team_id:
            message += f" team ID: {team_id}"
        if tricode:
            message += f" tricode: {tricode}"
        super().__init__(message)
