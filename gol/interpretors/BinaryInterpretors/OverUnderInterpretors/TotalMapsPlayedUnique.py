from .OverUnderInterpretor import OverUnderInterpretor

class TotalMapsPlayedUnique(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totalmapsplayed"

    @classmethod
    def get_categorie(cls):
        return "global"

    def __call__(self, line):
        if line['action'] == 'nexus':
            self.counter += 1