from .OverUnderInterpretor import OverUnderInterpretor

class TotalKillsUnique(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totalkills"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'kill':
            self.counter += 1


class TotalKillsT1(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "t1_totalkills"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'kill' and line['team'] == "t1":
            self.counter += 1


class TotalKillsT2(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "t2_totalkills"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'kill' and line['team'] == "t2":
            self.counter += 1