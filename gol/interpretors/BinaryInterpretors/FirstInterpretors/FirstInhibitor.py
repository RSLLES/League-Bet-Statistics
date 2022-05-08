from .FirstInterpretor import FirstInterpretor

class FirstInhibitor(FirstInterpretor):
    @classmethod
    def get_name(cls):
        return "destroyfirstinhibitor"
    
    @classmethod
    def objectif_name(self):
        return "inhib"