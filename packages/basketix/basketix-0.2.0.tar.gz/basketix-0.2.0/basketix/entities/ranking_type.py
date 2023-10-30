"""Ranking type module"""
from enum import Enum

class RankingType(str, Enum):
    """Ranking type class"""

    POINTS = 'POINTS'
    EVALUATIONS = 'EVALUATIONS'
