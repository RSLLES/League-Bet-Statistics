from .FirstInterpretor import FirstInterpretor

class FirstTower(FirstInterpretor):
    @classmethod
    def get_name(cls):
        return "destroyfirsttower"
    
    @classmethod
    def objectif_name(self):
        return "tower"