from .OverUnderInterpretor import OverUnderInterpretor

class TotalTowers(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totaltowersslain"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'tower':
            self.counter += 1
