'''Transactions entities module'''

class Transactions():
    GAME_CONFIG = 'GameConfig'
    DRAFT_PICK = 'DraftPick'
    FREE_AGENCY = 'FreeAgency'

    #Free Agency
    BID = 'FreeAgency_Bid'
    BID_DELETE = 'FreeAgency_BidDelete'
    BID_LOOSE = 'FreeAgency_loose'
    BID_WIN = 'FreeAgency_win'
    CUT = 'FreeAgency_Cut'
