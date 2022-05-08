from .OverUnderInterpretor import OverUnderInterpretor

class TotalBarons(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totalbaronsslain"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'nashor':
            self.counter += 1
