"""Basketix seasons module"""

from typing import Dict, List, Optional, Tuple, Union

from .basketix_weeks import BasketixWeeksHandler

from ..entities import NbaPlayersMotions, Transactions, BasketixError, LeagueStatus, RankingType, BasketixDate
from ..helpers import DateHelper, uid
from ..tables import BasketixSeasonsTable

class BasketixSeasonsHandler:
    """Handle basketix seasons"""

    BEGIN_DAY_OF_WEEK: str = 'monday'
    DEFAULT_SALARY_CAP = 100
    DEFAULT_DRAFT_PICK_SECOND_DELAY = 5*60
    MIN_DRAFT_DELAY_SECONDS = 30
    DEFAULT_RANKING_TYPE = RankingType.POINTS
    DEFAULT_N_SUBSTITUTE = 2
    DEFAULT_POINTS_TABLE = {
        '1': 20,
        '2': 16,
        '3': 13,
        '4': 11,
        '5': 10,
        '6': 9,
        '7': 8,
        '8': 7,
        '9': 6,
        '10': 5,
        '11': 4,
        '12': 3,
        '13': 2,
        '14': 1,
    }
    DEFAULT_BEST_PLAYER_BONUS_POINT = 1
    DEFAULT_BEST_GAME_BONUS_POINT = 1

    def __init__(self, environment: str) -> None:
        """Init basketix season handler"""

        self.basketix_seasons_table = BasketixSeasonsTable(environment)
        self.basketix_weeks_handler = BasketixWeeksHandler(environment)

    def get(self, season_id: str) -> dict:
        """Returns the season corresponding"""

        return self.basketix_seasons_table.query(season_id)[0]

    def get_status(self, season_id: Optional[str] = None, season: Optional[dict] = None) -> str:
        """Returns the status of the season"""

        if not season:
            season_id = season_id if season_id else ''
            season = self.get(season_id)

        if not season['seasonStatus']['draft']['isFinished']:
            return LeagueStatus.DRAFT
        if self._is_regular_season_finished(season.get('regularSeason', {})):
            return LeagueStatus.FINISHED

        return LeagueStatus.REGULAR_SEASON

    def get_number_of_members(self, season_id: str) -> int:
        """Returns the number of users in the season"""

        return len(self.get(season_id)['basketixs'])

    def get_next_season_settings(self, season_id: str) -> dict:
        """Returns the default settings for the next season"""

        season = self.get(season_id)

        return {
            'salaryCap': season['salaryCap'],
            'draftType': season['draft']['nextDraftType'],
            'isDraftReverse': season['draft']['nextDraftIsReverse'],
            'nDraftRound':  season['draft']['nRound'],
            'draftPickSecondDelay': season['draft']['draftPickSecondDelay'],
            'nWeek': season['regularSeason']['nWeeks'],
            'nSubstitute': season['regularSeason']['nSubstitute'],
            'rankingType': season['regularSeason']['rankingType'],
            'pointsTable': season['regularSeason']['pointsTable'],
        }

    def create_season(self,
                    league_id: str,
                    n_week: int,
                    ranking_type: Optional[RankingType],
                    draft_order: list,
                    n_round_draft: int,
                    draft_type: str,
                    is_draft_reverse: bool,
                    draft_pick_second_delay: Optional[int],
                    players: dict,
                    salary_cap: Optional[int],
                    points_table: Optional[Dict[str, int]],
                    next_season_draft_type: str,
                    next_season_is_draft_reverse: bool,
                    n_substitute: Optional[int],
                    best_player_bonus_points: Optional[int],
                    best_game_bonus_points: Optional[int]) -> dict:
        """Create a new season"""

        ranking_type = ranking_type if ranking_type else self.DEFAULT_RANKING_TYPE
        salary_cap = salary_cap if salary_cap is not None else self.DEFAULT_SALARY_CAP
        draft_pick_second_delay = draft_pick_second_delay if draft_pick_second_delay else self.MIN_DRAFT_DELAY_SECONDS
        n_substitute = n_substitute if n_substitute is not None else self.DEFAULT_N_SUBSTITUTE
        best_player_bonus_points = best_player_bonus_points if best_player_bonus_points is not None else self.DEFAULT_BEST_PLAYER_BONUS_POINT
        best_game_bonus_points = best_game_bonus_points if best_game_bonus_points is not None else self.DEFAULT_BEST_GAME_BONUS_POINT

        if draft_pick_second_delay < self.MIN_DRAFT_DELAY_SECONDS:
            raise BasketixError('InvalidPickDelay', tokens={'min_delay': self.MIN_DRAFT_DELAY_SECONDS})

        if points_table:
            try:
                [(int(rank), int(pts)) for rank, pts in points_table.items()]
            except ValueError as err:
                raise BasketixError('InvalidPointsTable') from err
        else:
            points_table = self.DEFAULT_POINTS_TABLE

        season = {
            'seasonId': self._generate_season_id(),
            'leagueId': league_id,
            'creationDateTime': DateHelper.now(),
            'basketixIds': draft_order,
            'basketixs': {},
            'salaryCap': salary_cap,
            'draft': {
                'order': self._init_draft(draft_order, is_draft_reverse, n_round_draft),
                'players': players,
                'draftPickSecondDelay': draft_pick_second_delay,
                'draftType': draft_type,
                'isReverse': is_draft_reverse,
                'nRound': n_round_draft,
                'nextDraftType': next_season_draft_type,
                'nextDraftIsReverse': next_season_is_draft_reverse,
            },
            'regularSeason': {
                'rankingType': ranking_type,
                'nWeeks': n_week,
                'nSubstitute': n_substitute,
                'pointsTable': points_table,
                'bonusPoints': {
                    'bestPlayer': best_player_bonus_points,
                    'bestGame': best_game_bonus_points,
                }
            },
            'players': {},
            'seasonStatus': {}
        }

        for basketix_id in draft_order:
            season['basketixs'][basketix_id] = {
                'watchedPalyer': [],
                'transactions': [{
                    'type': Transactions.GAME_CONFIG,
                    'salaryCap': salary_cap,
                    'isSecret': False,
                }]
            }

        season['seasonStatus']['draft'] = self._update_draft_status(season['draft']['order'], 0, draft_pick_second_delay)

        self.basketix_seasons_table.insert([season])

        return season

    def pick_player(self, season_id: str, pick_number: int, basketix_id: str, player_id: Union[str, None]) -> dict:
        """Pick the player or skip the pick if no player"""

        season = self.basketix_seasons_table.query(season_id)[0]

        draft_status = season['seasonStatus']['draft']
        if draft_status['basketixId'] != basketix_id or draft_status['pickNumber'] != pick_number:
            raise BasketixError('CanNotPick')

        draft_pick_second_delay = season['draft']['draftPickSecondDelay']

        cost = season['draft']['players'][player_id]['cost'] if player_id else None
        positions = season['draft']['players'][player_id]['positions'] if player_id else None

        season = self._pick_player_recursive(season, pick_number, basketix_id, player_id, cost, positions, draft_pick_second_delay)
        self.basketix_seasons_table.update([season])

        return season['seasonStatus']['draft']

    def set_pre_draft_list(self, season_id: str, basketix_id: str, pick_number: int, player_ids: list, auto: bool) -> dict:
        """Set the pre-draft list of an user"""

        season = self.basketix_seasons_table.query(season_id)[0]

        if season['draft']['order'][pick_number - 1]['basketixId'] != basketix_id:
            raise BasketixError('InvalidPickNumber', tokens={'pick_number': pick_number})

        drafted_players = [pick['playerId'] for pick in season['draft']['order'] if 'playerId' in pick]
        already_drafted_players = list(set(drafted_players) & set(player_ids))
        if already_drafted_players:
            raise BasketixError('AlreadyDrafted')

        season['draft']['order'][pick_number - 1]['predraft']['choices'] = player_ids
        season['draft']['order'][pick_number - 1]['predraft']['auto'] = auto
        update_item = {'seasonId': season_id}
        update_item['draft'] = season['draft']
        self.basketix_seasons_table.update([update_item])

        return season['draft']['order'][pick_number - 1]

    def get_roster(self, season_id: str, basketix_id: str, week_id: str) -> dict:
        """Get players positions and costs from basketix rosters"""

        roster = {}
        for player_id, player_history in self._get_players(season_id=season_id).items():
            player_motion = self.get_owner_and_info(week_id, player_history)
            if player_motion and player_motion['basketixId'] == basketix_id:
                roster[player_id] = {
                    'basketixId': basketix_id,
                    'playerId': player_id,
                    'cost': player_motion['cost'],
                    'positions': player_motion['positions'],
                }

        return roster

    def players_in_roster(self, basketix_id: str, week_id: str, player_ids: List[str], season_id: Optional[str] = None, players: Optional[dict] = None):
        """Returns only the players_ids who are parts of the basketix roster for the weekId"""

        player_ids_in_roster = []
        if not players:
            players = self._get_players(season_id=season_id)

        for player_id in player_ids:
            owner = self.get_owner_and_info(week_id, players[player_id])
            if owner and owner['basketixId'] == basketix_id:
                player_ids_in_roster.append(player_id)

        return player_ids_in_roster

    def get_all_players(self, season_id: str, week_id: str) -> dict:
        """Returns all players with owner"""

        season = self.basketix_seasons_table.query(season_id)[0]
        players = self._get_players(season=season)

        players_with_owner = {}
        for player_id, player_history in players.items():
            player_motion = self.get_owner_and_info(week_id, player_history)
            if player_motion and 'basketixId' in player_motion:
                players_with_owner[player_id] = {key: player_motion[key] for key in ['positions', 'cost', 'basketixId']}

        return players_with_owner

    def is_season_finished(self, season_id: str) -> bool:
        """Check if season is finished"""

        season = self.basketix_seasons_table.query(season_id)[0]

        is_draft_finished = self._is_draft_finished(season['draft']['order'])
        is_regular_season_finished = self._is_regular_season_finished(season['regularSeason'])

        return is_draft_finished and is_regular_season_finished

    def get_cap_space(self, transcations: list, with_secrets: bool) -> Tuple[int, Optional[int]]:
        """
        Returns a tuple of :
        - the salary cap based on transactions (with or without secret transactions)
        - the public salary cap if with_secrets = True else None
        """

        salary_cap_transactions = []
        secret_transactions = [0]
        for transaction in transcations:
            if 'salaryCap' in transaction and transaction.get('isSecret', False) in (False, with_secrets):
                salary_cap_transactions.append(transaction['salaryCap'])

            if 'salaryCap' in transaction and transaction.get('isSecret'):
                secret_transactions.append(transaction['salaryCap'])

        return sum(salary_cap_transactions), sum(salary_cap_transactions) - sum(secret_transactions) if with_secrets else None

    #Deprecated
    def filter_teams_players(self, basketix_teams: List[dict]) -> List[dict]:
        """Delete NBA players who are not in the basketix roster"""

        season_ids = list(set([team['seasonId'] for team in basketix_teams]))

        filtered_teams = []
        for season_id in season_ids:
            teams = [team for team in basketix_teams if team['seasonId'] == season_id]
            season_players = self._get_players(season_id)
            for team in teams:
                filter_team = self._delete_players_not_in_roster(team, season_players)
                filtered_teams.append(filter_team)

        return filtered_teams

    def get_all_next_week_ids(self, week_id: str, season: dict) -> List[str]:
        """Return all the next weeks from <week_id>"""
        try:
            week_ids = season['regularSeason']['weekIds']
            return week_ids[week_ids.index(week_id, ):]
        except (KeyError, ValueError):
            return []

    #Deprecated
    def _delete_players_not_in_roster(self, team: dict, season_players: dict):
        """Init the position for NBA players who are not in the basketix roster"""

        player_ids = [player_id for player_id, _ in team['players'].items()]
        player_ids_in_roster = self.players_in_roster(team['basketixId'], team['weekId'], player_ids, players=season_players)
        player_id_not_in_roster = list(set(player_ids) - set(player_ids_in_roster))
        for player_id in player_id_not_in_roster:
            team['players'].pop(player_id)

        return team

    def _init_draft(self, draft_order: list, is_reverse: bool, n_round_draft: int) -> list:
        """Init draft"""

        n_basketix = len(draft_order)
        return [self._init_pick(basketix_id, i+1, n_basketix) for i, basketix_id in enumerate(self._get_all_draft_order(draft_order, is_reverse, n_round_draft))]

    def _pick_player_recursive(self, season: dict, pick_number: int, basketix_id: str, player_id: Optional[str], cost: Optional[int], positions: Optional[list], draft_pick_second_delay: int) -> dict:
        """Pick a player and the next ones if possible. Update season status"""

        utc_now = DateHelper.now()
        pick = season['draft']['order'][pick_number - 1]
        pick_update_base = {'engagementDateTime': utc_now, 'basketixId': basketix_id, 'isPick': True}

        if not player_id or not self._can_pick(basketix_id, season):
            pick.pop('predraft')
            pick.update(pick_update_base)
            return self._next_pick(season, pick_number, draft_pick_second_delay)

        if not self._can_pick_this_player(basketix_id, season, player_id):
            raise BasketixError('CanNotPick')

        pick.pop('predraft')
        pick.update(pick_update_base)
        pick.update({'playerId': player_id, 'cost': cost, 'positions': positions})

        player_histories = [{
            'date': utc_now,
            'type': NbaPlayersMotions.DRAFT,
            'basketixId': basketix_id,
            'cost': cost,
            'positions': positions,
        }]
        season['players'][player_id] = player_histories

        season['basketixs'][basketix_id]['transactions'].append({
            'type': Transactions.DRAFT_PICK,
            'playerId': player_id,
            'salaryCap': -cost,
            'isSecret': False,
        })

        return self._next_pick(season, pick_number, draft_pick_second_delay)

    def _next_pick(self, season: dict, pick_number: int, draft_pick_second_delay: int):
        season['seasonStatus']['draft'] = self._update_draft_status(season['draft']['order'], pick_number, draft_pick_second_delay)

        if season['seasonStatus']['draft']['isFinished']:
            season = self._close_draft(season)
            season = self._init_regular_season(season)
        else:
            next_basketix_id = season['seasonStatus']['draft']['basketixId']
            next_pick_number = season['seasonStatus']['draft']['pickNumber']

            if not self._can_pick(next_basketix_id, season):
                season = self._pick_player_recursive(season, next_pick_number, next_basketix_id, None, None, None, draft_pick_second_delay)
                return season

            predraft = season['draft']['order'][next_pick_number - 1]['predraft']
            if predraft['auto']:
                for pick_player_id in predraft['choices']:
                    if self._can_pick_this_player(next_basketix_id, season, pick_player_id): #TODO: A tester
                        next_positions = season['draft']['players'][pick_player_id]['positions']
                        next_cost = season['draft']['players'][pick_player_id]['cost']
                        season = self._pick_player_recursive(season, next_pick_number, next_basketix_id, pick_player_id, next_cost, next_positions, draft_pick_second_delay)
                        break

        return season

    def _update_draft_status(self, draft: list, actual_pick_number: int, draft_pick_second_delay: int) -> dict:
        """Returns if it's the turn of a specific player to pick a player during the draft"""

        is_finished = self._is_draft_finished(draft)
        draft_status = {'isFinished': is_finished}
        if not is_finished:
            # Next pick number
            draft_status = {
                **draft_status,
                'basketixId': draft[actual_pick_number]['basketixId'],
                'pickNumber': draft[actual_pick_number]['pickNumber'],
                'round': draft[actual_pick_number]['round'],
                'roundPick': draft[actual_pick_number]['roundPick'],
                'limitDateTime': DateHelper.now_delta(seconds=draft_pick_second_delay)
            }

        return draft_status

    def _init_regular_season(self, season: dict) -> dict:
        """Init a regular season after the draft is finished"""

        if self._is_draft_finished(season['draft']['order']):
            season_week_ids = self._get_season_week_ids(season['regularSeason']['nWeeks'])
            season['regularSeason'] = {
                **season['regularSeason'],
                'beginWeekId': season_week_ids[0],
                'endWeekId': season_week_ids[-1],
                'weekIds': season_week_ids,
            }
            season['seasonStatus']['regularSeason'] = self._update_regular_season_status(season['regularSeason'])

        return season

    def _update_regular_season_status(self, regular_season: dict) -> dict:
        """Update regular season status"""

        return {'isFinished': self._is_regular_season_finished(regular_season)}

    def _is_draft_finished(self, draft: list) -> bool:
        """Check if draft is finished"""
        return draft[-1]['isPick']

    def _is_regular_season_finished(self, regular_season: dict) -> bool:
        """Check if regular season is finished"""

        if 'weekIds' in regular_season:
            return self.basketix_weeks_handler.are_all_finished(regular_season['weekIds'])

        return False

    def get_owner_and_info(self, week_id: str, history: list) -> Optional[dict]:
        """
        Finds basketix owner for a player motion history and a <week_id>
        and returns players main info (cost, positions, owner)
        """

        if 'lastWeekId' in history[-1] and 'lastWeekId' in history[-1] and week_id > history[-1]['lastWeekId']:
            return None

        for motion in reversed(history):
            if 'lastWeekId' in motion and 'firstWeekId' in motion and motion['firstWeekId'] <= week_id <= motion["lastWeekId"]:
                return motion

            if 'lastWeekId' in motion and 'firstWeekId' not in motion and week_id <= motion["lastWeekId"]:
                return motion

            if not 'lastWeekId' in motion and 'firstWeekId' in motion and motion['firstWeekId'] <= week_id:
                return motion

        if history[0]['type'] == 'Draft' and (not 'lastWeekId' in history[0] or week_id <= history[0]['lastWeekId']):
            return history[0]

        return None

    def _get_players(self, season_id: Optional[str] = None, season: Optional[dict] = None) -> dict:
        """Get players positions and costs from all basketix rosters"""

        if season_id:
            season = self.basketix_seasons_table.query(season_id)[0]
        elif not season:
            raise BasketixError('InvalidSeason')

        return season['players']

    def _close_draft(self, season: dict):
        """Close draft when it is finish. Delete none drafted player"""

        season['draft'].pop('players', season)

        return season

    def _generate_season_id(self) -> str:
        """Generate a season id"""

        return uid()

    def _get_all_draft_order(self, draft_order: list, is_reverse: bool, n_round_draft: int) -> list:
        """Returns ordered basketix id list of the draft"""

        draft_orders = [draft_order for _ in range(n_round_draft)]

        if is_reverse:
            for _round, _ in enumerate(draft_orders):
                if _round % 2 == 1:
                    draft_orders[_round] = list(reversed(draft_orders[_round]))

        return [_round for draft_round in draft_orders for _round in draft_round]

    def _init_pick(self, basketix_id: str, position: int, n_basketix: int):
        """Init a draft pick"""

        return {
            'basketixId': basketix_id,
            'isPick': False,
            'pickNumber': position,
            'round': ((position - 1) // n_basketix) + 1,
            'roundPick': position - (n_basketix * (((position - 1) // n_basketix))),
            'predraft': {
                'auto': True,
                'choices': []
            }
        }

    def _can_pick(self, basketix_id: str, season: dict) -> bool:
        """Check if basketix has cap space i.e he can draft a player"""

        return self.get_cap_space(season['basketixs'][basketix_id]['transactions'], with_secrets=True)[0] > 0

    #TODO: A tester
    def _can_pick_this_player(self, basketix_id: str, season: dict, player_id: str) -> bool:
        """
        Check if basketix <basketix_id> can pick player <player_id> dependending
        of the draft history and basketix cap space
        """
        already_drafted_players = [player_id for player_id, _ in season['players'].items()]
        if player_id in already_drafted_players:
            return False

        cap_space, _ = self.get_cap_space(season['basketixs'][basketix_id]['transactions'], with_secrets=True)
        if cap_space == 0 or cap_space < season['draft']['players'][player_id]['cost']:
            return False

        return True

    def _get_season_week_ids(self, n_week: int) -> list:
        """Returns the list of weeks id for the regular season based on now"""

        first_week = BasketixDate.tomorrow().week.next()
        return [first_week.next(i).id for i in range(n_week)]
