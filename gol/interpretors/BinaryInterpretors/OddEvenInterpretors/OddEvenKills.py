from .OddEvenInterpretor import OddEvenInterpretor

class OddEvenKills(OddEvenInterpretor):
    @classmethod
    def get_name(cls):
        return "oddevenkills"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'kill':
            self.counter += 1