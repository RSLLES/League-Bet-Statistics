from ..BaseInterpretor import BaseInterpretor

class MultipleOverUnderInterpretor(BaseInterpretor):
    def __init__(self, match_bet, UniqueInterpretor) -> None:
        super().__init__(match_bet)
        values = self.get_both_options()
        def build_artifical_match_bet(v):
            d = {}
            d[self.get_categorie()] = {}
            o, u = "over" + str(v), "under" + str(v)
            d[self.get_categorie()][self.get_name()] = {
                o : match_bet[self.cat][self.name][o],
                u : match_bet[self.cat][self.name][u]
            }
            return d

        self.sub_inters = [
            UniqueInterpretor(build_artifical_match_bet(v))
            for v in values
        ]

    def reset(self):
        for t in self.sub_inters:
            t.reset()

    def __call__(self, line):
        for t in self.sub_inters:
            t(line)

    def export(self):
        l = {}
        for t in self.sub_inters:
            l = {**l, **(t.export()[self.get_name()])}
        return {self.get_name() : l}

    def get_both_options(self):
        values = set()
        for obj in self.odds:
            assert "over" in obj or "under" in obj, f"{self.odds} must all include 'over' or 'under'"
            value = float(obj.replace("over", "").replace("under", ""))
            values.add(value)
        
        return list(values)