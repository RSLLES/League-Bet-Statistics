from ..BinaryInterpretor import BinaryInterpretor

class OddEvenInterpretor(BinaryInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet)
        opt1, opt2 = self.get_both_options()
        assert "odd" == opt1 and "even" == opt2, f"{self.get_both_options()} should be 'odd' and 'even'"
        self.counter = 0

    def reset(self):
        super().reset()
        self.counter = 0

    def export(self):
        if self.counter % 2 == 1:
            self.winner = self.get_both_options()[0]
        else:
            self.winner = self.get_both_options()[1]
        return super().export()