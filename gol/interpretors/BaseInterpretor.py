class BaseInterpretor:
    def __init__(self, match_bet) -> None:
        self.name = self.get_name()
        self.cat = self.get_categorie()
        self.odds = match_bet[self.cat][self.name]
        self.def_odds = match_bet[self.cat][self.name].copy()

    def reset(self):
        self.odds = self.def_odds.copy()

    @classmethod
    def isPresent(cls, match_bet):
        return cls.get_name() in match_bet[cls.get_categorie()]

    @classmethod
    def get_name(cls):
        raise NotImplementedError()
    
    @classmethod
    def get_categorie(cls):
        raise NotImplementedError()

    def __call__(self, line):
        raise NotImplementedError()

    def export(self):
        raise NotImplementedError()
