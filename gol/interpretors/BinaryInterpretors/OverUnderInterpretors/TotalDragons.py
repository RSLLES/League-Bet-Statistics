from .OverUnderInterpretor import OverUnderInterpretor

class TotalDragons(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totalelementaldragonsslain"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'drake':
            self.counter += 1
