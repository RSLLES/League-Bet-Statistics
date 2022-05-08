from .MultipleOverUnderInterpretor import MultipleOverUnderInterpretor
from ..BinaryInterpretors.OverUnderInterpretors.TotalKills import TotalKillsUnique

class TotalKills(MultipleOverUnderInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet, TotalKillsUnique)
    
    @classmethod
    def get_name(cls):
        return "totalkills"
    
    @classmethod
    def get_categorie(cls):
        return "map"