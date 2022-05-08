from ..BinaryInterpretor import BinaryInterpretor

class OverUnderInterpretor(BinaryInterpretor):
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet)
        opt1, opt2 = self.get_both_options()
        assert "over" in opt1 and "under" in opt2, f"{self.get_both_options()} must respectively contain 'over' and 'under'"
        v1, v2 = self.format_string_to_float(opt1.replace("over", "")), self.format_string_to_float(opt2.replace("under", ""))
        assert v1 == v2, f"Both over and under must tackle the same value. Here with {self.get_both_options()} it founds {(v1, v2)}"
        self.threshold = v1
        self.counter = 0

    def reset(self):
        self.counter = 0
        return super().reset()
    
    @classmethod
    def format_string_to_float(self, text):
        return float(text)

    def export(self):
        if self.counter > self.threshold:
            self.winner = self.get_both_options()[0]
        elif self.counter < self.threshold:
            self.winner = self.get_both_options()[1]
        else:
            raise ValueError("Counter is equal to threshold : can't choose between over and under !")
        return super().export()