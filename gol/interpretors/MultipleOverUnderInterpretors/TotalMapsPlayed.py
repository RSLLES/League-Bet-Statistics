from .MultipleOverUnderInterpretor import MultipleOverUnderInterpretor
from ..BinaryInterpretors.OverUnderInterpretors.TotalMapsPlayedUnique import TotalMapsPlayedUnique

class TotalMapsPlayed(MultipleOverUnderInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet, TotalMapsPlayedUnique)
    
    @classmethod
    def get_name(cls):
        return "totalmapsplayed"
    
    @classmethod
    def get_categorie(cls):
        return "global"