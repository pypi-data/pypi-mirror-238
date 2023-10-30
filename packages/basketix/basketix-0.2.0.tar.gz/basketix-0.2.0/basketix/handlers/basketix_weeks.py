"""WeekId helper module"""

from typing import List, Optional

from ..entities import BasketixError
from ..helpers import DateHelper
from ..tables import BasketixWeeksTable

class BasketixWeeksHandler:

    def __init__(self, environment: str) -> None:
        self.basketix_weeks_table = BasketixWeeksTable(environment)

    def are_all_finished(self, week_ids: List[str]) -> bool:
        """Returns if all week_id in week_ids are finished"""

        for week_id in week_ids:
            week_res = self.basketix_weeks_table.query(week_id)
            if not week_res:
                return False
            all_days_finished = week_res[0].get('isAllDaysFinished', False)
            if not all_days_finished:
                return False

        return True

    def get_start_time_utc(self, week_id: str) -> Optional[str]:
        """Returns the start time (UTC) for a week id"""

        weeks = self.basketix_weeks_table.query(week_id)
        if weeks:
            return weeks[0].get('startTimeUTC')

        return None

    def is_week_started(self, week_id: Optional[str] = None, week: Optional[dict] = None) -> bool:
        """Returns if the week is started or not"""

        week = self._get_week(week_id, week)
        if not week:
            return False

        start_time_utc: Optional[str] = week.get('startTimeUTC')
        if not start_time_utc:
            return False

        utc_now = DateHelper.now()

        return utc_now >= start_time_utc

    def is_week_finished(self, week_id: Optional[str] = None, week: Optional[dict] = None) -> bool:
        """Returns if the week is finished or not"""

        week = self._get_week(week_id, week)
        if not week:
            return False

        is_finished = week.get('isFinished')

        if is_finished is None:
            return False

        return is_finished

    def is_week_live(self, week_id: Optional[str] = None, week: Optional[dict] = None) -> bool:
        """Returns if the week is live or not"""

        week = self._get_week(week_id, week)
        if not week:
            return False

        return self.is_week_started(week=week) and not self.is_week_finished(week=week)

    def get_week_status(self, week_id: str) -> dict:
        """Returns if week is starter, finished and live"""

        weeks = self.basketix_weeks_table.query(week_id)
        if not weeks:
            return {
                'weekId': week_id,
                'isStarted': False,
                'isFinished': False,
                'isLive': False,
            }

        week = weeks[0]
        return {
            'weekId': week_id,
            'isStarted': self.is_week_started(week=week),
            'isFinished': self.is_week_finished(week=week),
            'isLive': self.is_week_live(week=week),
            'startTimeUTC': week['startTimeUTC'],
        }

    def get_weeks_status(self, week_ids: List[str]) -> List[dict]:
        """Returns if weeks are starter, finished and live"""

        return [self.get_week_status(week_id) for week_id in week_ids]

    def _get_week(self, week_id: Optional[str], week: Optional[dict] = None) -> Optional[dict]:
        """Queries week if necessary and returns it"""
        if not week_id and not week:
            raise BasketixError('InvalidParameters')

        if not week:
            weeks = self.basketix_weeks_table.query(week_id)
            if not weeks:
                return None
            week = weeks[0]

        return week
