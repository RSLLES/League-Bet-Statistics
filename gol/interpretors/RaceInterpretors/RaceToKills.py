from .RaceInterpretor import RaceInterpretor

class RaceToKills(RaceInterpretor):
    @classmethod
    def get_name(cls):
        return "racetokills"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    @staticmethod
    def format_time_to_float(text):
        return float(text.replace(":", "."))

    def __call__(self, line):
        if line["action"] == "kill":
            self.timed_events.append((RaceToKills.format_time_to_float(line["time"]), line["team"]))