'''League status entities module'''

TRADUCTION = {
    'WAITING': {
        'en': 'Waiting',
        'fr': 'En attente'
    },
    'DRAFT': {
        'en': 'Draft',
        'fr': 'Draft'
    },
    'REGULARSEASON': {
        'en': 'Regular season',
        'fr': 'Saison régulière'
    },
    'FINISHED': {
        'en': 'Finished',
        'fr': 'Terminée'
    },
}

class LeagueStatus():
    '''League status'''

    WAITING = 'WAITING'
    DRAFT = 'DRAFT'
    REGULAR_SEASON = 'REGULARSEASON'
    FINISHED = 'FINISHED'

    @classmethod
    def translate(cls, status: str, language: str = 'en'):
        '''Translate a league status'''
        return TRADUCTION[status][language]
