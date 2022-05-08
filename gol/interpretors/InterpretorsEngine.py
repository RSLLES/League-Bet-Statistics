from .BinaryInterpretors.GameWinner import GameWinner
from .BinaryInterpretors.MatchWinner import MatchWinner

from .BinaryInterpretors.FirstInterpretors.FirstBaron import FirstBaron
from .BinaryInterpretors.FirstInterpretors.FirstBlood import FirstBlood
from .BinaryInterpretors.FirstInterpretors.FirstDragon import FirstDragon
from .BinaryInterpretors.FirstInterpretors.FirstHerald import FirstHerald
from .BinaryInterpretors.FirstInterpretors.FirstInhibitor import FirstInhibitor
from .BinaryInterpretors.FirstInterpretors.FirstTower import FirstTower

from .BinaryInterpretors.OddEvenInterpretors.OddEvenKills import OddEvenKills

from .BinaryInterpretors.OverUnderInterpretors.TotalBarons import TotalBarons
from .BinaryInterpretors.OverUnderInterpretors.TotalDragons import TotalDragons
from .BinaryInterpretors.OverUnderInterpretors.TotalKills import TotalKillsT1, TotalKillsT2
from .BinaryInterpretors.OverUnderInterpretors.TotalTime import TotalTime
from .BinaryInterpretors.OverUnderInterpretors.TotalTowers import TotalTowers

from .RaceInterpretors.RaceToKills import RaceToKills

from .MultipleOverUnderInterpretors.TotalKills import TotalKills
from .MultipleOverUnderInterpretors.TotalMapsPlayed import TotalMapsPlayed


class InterpretorsEngine:
    def __init__(self, match_bet) -> None:
        # Recuperation des noms
        self.teamsNames = match_bet['teamNames']
        self.date = match_bet['date']
        self.bolength = match_bet['BOLength']
        self.games = {}
        self.game_idx = 1

        self.all_existing_interpretors = [
            FirstBaron,
            FirstBlood,
            FirstDragon,
            FirstHerald,
            FirstInhibitor,
            FirstTower,
            GameWinner,
            MatchWinner,
            OddEvenKills,
            RaceToKills,
            TotalBarons,
            TotalDragons,
            TotalKills,
            TotalKillsT1,
            TotalKillsT2,
            TotalMapsPlayed,
            TotalTime,
            TotalTowers
        ]

        self.activated_interpretors = []
        for InterpretorClass in self.all_existing_interpretors:
            if InterpretorClass.isPresent(match_bet):
                self.activated_interpretors.append(InterpretorClass)
        print(f"List of activated interpretors : {list(map(lambda x : x.get_name(), self.activated_interpretors))}")

        # Creation des objets utiles
        self.activated_interpretors = list(map(lambda Interpretor : Interpretor(match_bet), self.activated_interpretors))

    def next_game(self):
        self.games[f"map{self.game_idx}"] = {}
        for interpretor in self.activated_interpretors:
            if interpretor.get_categorie() == "map":
                self.games[f"map{self.game_idx}"] = {**interpretor.export(), **self.games[f"map{self.game_idx}"]}
                interpretor.reset()
        if not self.games[f"map{self.game_idx}"]:
            self.games.pop(f"map{self.game_idx}")
        self.game_idx += 1

    def build_global(self):
        self.games["global"] = {}
        for interpretor in self.activated_interpretors:
            if interpretor.get_categorie() == "global":
                self.games["global"] = {**interpretor.export(), **self.games["global"]}

    def __call__(self, line):
        for interpretor in self.activated_interpretors:
            interpretor(line)

    def teams(self):
        return self.teamsNames

    def export(self):
        match_bet = {
            "teamNames" : self.teamsNames,
            "date" : self.date,
            "BOLength" : self.bolength
        }

        self.build_global()
        match_bet = {**match_bet, **self.games}
        return match_bet