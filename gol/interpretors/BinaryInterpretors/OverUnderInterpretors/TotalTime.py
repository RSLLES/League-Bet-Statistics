from .OverUnderInterpretor import OverUnderInterpretor

class TotalTime(OverUnderInterpretor):
    @classmethod
    def get_name(cls):
        return "totaltime"
    
    @classmethod
    def get_categorie(cls):
        return "map"

    @staticmethod
    def edit_date_string(text):
        return text.replace(":", ".")
    
    @classmethod
    def format_string_to_float(cls, text):
        return super().format_string_to_float(TotalTime.edit_date_string(text))

    def __call__(self, line):
        if line['action'] == 'nexus':
            self.counter = self.format_string_to_float(line['time'])*100