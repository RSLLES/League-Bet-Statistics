from ..BaseInterpretor import BaseInterpretor

class BinaryInterpretor (BaseInterpretor) :
    def get_both_options(self):
        assert len(list(self.odds)) == 2, f"BinaryInterpretors must only have 2 valids bet, here there is {len(list(self.odds))} : {list(self.odds)}"
        return list(self.odds)
        
    def export(self):
        opt1, opt2 = self.get_both_options()
        if self.winner == opt1 :
            self.loser = opt2
        elif self.winner == opt2 :
            self.loser = opt1
        else:
            raise ValueError(f"{self.winner} should be in {self.get_both_options()}")

        self.odds[self.winner]  =   (self.odds[self.winner],    True)
        self.odds[self.loser]   =   (self.odds[self.loser],     False)
        return {self.name : self.odds}