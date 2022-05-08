from ..BaseInterpretor import BaseInterpretor

class RaceInterpretor (BaseInterpretor) :
    def __init__(self, match_bet) -> None:
        super().__init__(match_bet)
        # Decomposition des odds
        self.time_markers = set()
        for key in self.odds:
            assert "_" in key, f"{key} should be in the following format : $team_$timeMarker" 
            team, time_marker = key.split("_")
            assert f"{RaceInterpretor.other(team)}_{time_marker}" in self.odds, f"Found {key} but can't find {RaceInterpretor.other(team)}_{time_marker} in {self.odds}"
            self.time_markers.add(float(time_marker))
        self.time_markers = sorted(self.time_markers)
        self.timed_events = []

    @staticmethod
    def other (t):
        if t == "t1":
            return "t2"
        if t == "t2":
            return "t1"
        raise ValueError()

    def export(self):
        self.cumul_sum = {"t1" : 0, "t2" : 0}
        i = 0
        for time, team in self.timed_events:
            if i < len(self.time_markers) and time > self.time_markers[i]:
                wint1 = self.cumul_sum["t1"] > self.cumul_sum["t2"]
                wint2 = self.cumul_sum["t2"] > self.cumul_sum["t1"]
                time = int(self.time_markers[i]) if self.time_markers[i].is_integer() else self.time_markers[i]
                self.odds[f"t1_{time}"] = (self.odds[f"t1_{time}"], wint1)
                self.odds[f"t2_{time}"] = (self.odds[f"t2_{time}"], wint2)
                i+=1
            self.cumul_sum[team] += 1

        # Remove too high best
        while i < len(self.time_markers):
            time = int(self.time_markers[i]) if self.time_markers[i].is_integer() else self.time_markers[i]
            self.odds.pop(f"t1_{time}")
            self.odds.pop(f"t2_{time}")
            i+=1
        return {self.name : self.odds}