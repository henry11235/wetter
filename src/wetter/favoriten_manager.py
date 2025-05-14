import json
import os

class favoriten_manager:
    def __init__(self, dateipfad="favoriten.json"):
        self.dateipfad = dateipfad
        self.favoriten = []
        self.lade_favoriten()

    def lade_favoriten(self):
        if os.path.exists(self.dateipfad):
            try:
                with open(self.dateipfad, "r") as f:
                    self.favoriten = json.load(f)
            except:
                self.favoriten = []

    def speichere_favoriten(self):
        try:
            with open(self.dateipfad, "w") as f:
                json.dump(self.favoriten, f)
        except:
            pass

    def hinzufuegen(self, ort):
        if ort and ort not in self.favoriten:
            self.favoriten.append(ort)
            self.speichere_favoriten()

    def entfernen(self, ort):
        if ort in self.favoriten:
            self.favoriten.remove(ort)
            self.speichere_favoriten()

    def gib_favoriten(self):
        return self.favoriten 