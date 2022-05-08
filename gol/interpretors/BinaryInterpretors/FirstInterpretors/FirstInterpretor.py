from ..BinaryInterpretor import BinaryInterpretor

class FirstInterpretor(BinaryInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet)
        self.firstEncounter = True
    
    @classmethod
    def get_categorie(cls):
        return "map"

    def reset(self):
        super().reset()
        self.firstEncounter = True

    @classmethod
    def objectif_name(self):
        raise NotImplementedError()

    def __call__(self, line):
        if self.firstEncounter and line['action'] == self.objectif_name():
            self.winner = line['team'] + "_"
            self.firstEncounter = False