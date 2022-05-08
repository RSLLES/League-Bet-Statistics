from .BinaryInterpretor import BinaryInterpretor

class GameWinner(BinaryInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet)
        self.wins = 0

    @classmethod
    def get_name(cls):
        return "matchwinner"
    
    @classmethod
    def get_categorie(cls):
        return "global"

    def __call__(self, line):
        if line['action'] == 'nexus':
            if line['team'] == "t1":
                self.wins += 1
            elif line['team'] == "t2":
                self.wins -= 1
            else :
                raise ValueError(f"{line['team']} should be etiher 't1' or 't2'")

    def export(self):
        if self.wins > 0:
            self.winner = "t1_"
        elif self.wins < 0:
            self.winner = "t2_"
        else:
            raise ValueError("No one wins !")
        return super().export()