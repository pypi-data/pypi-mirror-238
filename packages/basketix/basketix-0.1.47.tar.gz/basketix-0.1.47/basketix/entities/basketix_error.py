"""Basketix error module"""

import os
import traceback
from typing import Optional

from ..entities import DEFAULT_LANGUAGE

ENVIRONMENT = os.getenv('ENVIRONMENT', 'test')

class BasketixError(Exception):
    """Basketix error class"""

    ERROR_MESSAGES = {
        "UnknownError": {
            "en": "Unknown error",
            "fr": "Erreur inconnue"
        },
        "Unauthorized": {
            "en": "Not authorized",
            "fr": "Non autorisé"
        },
        "InvalidParameters": {
            "en": "Invalid parameters : { parameters_error }"
        },
        "NotFreeAgent": {
            "en": "The player is not a free agent in this season"
        },
        "InvalidBid_TooSmall": {
            "en": "Player is more expansive ({ player_cost }) than your bid ({ cost })"
        },
        "InvalidBid_CutRecently": {
            "en": "You cut the player less than { min_days_after_cut } days"
        },
        "InvalidBid_CapSpace": {
            "en": "You have not enougth cap space ({ cap_space }) for this bid ({ cost })"
        },
        "InvalidBid_LowerThanPrevious": {
            "en": "Your new bid must be superior than the older : { old_bid_cost }"
        },
        "InvalidWithdraw": {
            "en": "You did not bid for this player"
        },
        "InvalidOwner": {
            "en": "You are not the owner of the player"
        },
        "InvalidPickDelay": {
            "en": "Draft pick delay should be at least { min_delay } seconds"
        },
        "AlreadyInLeague": {
            "en": "Your already are in the league"
        },
        "AccessToLeagueDenied": {
            "en": "Access to the league denied"
        },
        "UnknownDraftType": {
            "en": "Unknown draft type"
        },
        "InvalidPickNumber": {
            "en": "Pick number { pick_number } if not yours pick"
        },
        "AlreadyDrafted": {
            "en": "Some players are already drafted"
        },
        "CanNotPick": {
            "en": "You can not pick the player"
        },
        "InvalidSeason": {
            "en": "Can not get season"
        },
        "TeamAlreadyExists": {
            "en": "A team already exists"
        },
        "InvalidPositionsTeam": {
            "en": "Player positions not allowed to build a team"
        },
        "InvalidEmail": {
            "en": "{ email } already used"
        },
        "InvalidConfirmationCode": {
            "en": "Confirmation code is not valid"
        },
        "PlayerWithoutCost": {
            "en": "Player { player_id } does not have a cost"
        },
        "InvalidEmailFormat": {
            "en": "Invalid email format"
        },
        "InvalidPasswordFormat": {
            "en": "Invalid password policy"
        },
        "InvalidPasswordConfirmation": {
            "en": "Passwords not identical"
        },
        "NotLeagueMember": {
            "en": "You are not a member of this league"
        },
        "NotFinishedSeason": {
            "en": "At least one season is not finished"
        },
        "StartedWeek": {
            "en": "This week is started"
        },
        "NotInRoster": {
            "en": "Some players are not in your roster for this week"
        },
        "FinishedDraft": {
            "en": "Draft is finished : can not find free agents"
        },
        "PlayerMustHaveOnePosition": {
            "en": "A player can have only one position",
            "fr": "Un joueur ne peut avoir qu'une seule position"
        },
        "InvalidPointsTable": {
            "en": "Invalid points table",
            "fr": "Tableau de points invalide"
        },
    }


    def __init__(self, error_code: str, tokens: Optional[dict] = None, inner_exception: Optional[Exception] = None, status_code=400):
        """Init the basketix error."""
        Exception.__init__(self)
        self.error_code = error_code
        self.error_message = None
        self.tokens: dict = tokens if tokens else {}
        self.status_code = status_code
        self._inner_exception = inner_exception

    def __str__(self):
        msg = f"BasketixError : {self.error_code}"
        if self._inner_exception is not None:
            trb = '\n'.join(traceback.format_exception(self._inner_exception.__class__,
                                                       self._inner_exception,
                                                       self._inner_exception.__traceback__))
            msg = msg + '\n' + trb
        return msg

    def get(self, language: Optional[str]) -> dict:
        error = {
            'type': 'BasketixError',
            'code': self.error_code,
            'message': self._error_message(language),
        }
        if ENVIRONMENT != 'prod':
            error['traceback'] = str(self)

        return error

    def _error_message(self, language: Optional[str]) -> str:
        language = language if language else DEFAULT_LANGUAGE
        messages = self.ERROR_MESSAGES[self.error_code]
        message = messages[language] if language in messages else messages[DEFAULT_LANGUAGE]

        for key, value in self.tokens.items():
            message = message.replace(f'{{ {key} }}', str(value))

        return message
