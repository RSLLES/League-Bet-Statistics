from .BinaryInterpretor import BinaryInterpretor

class MatchWinner(BinaryInterpretor):
    @classmethod
    def get_name(cls):
        return "winner"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def __call__(self, line):
        if line['action'] == 'nexus':
            self.winner = line['team'] + "_"