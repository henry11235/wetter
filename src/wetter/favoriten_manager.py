import json
import os
from pathlib import Path

class favoriten_manager:
    def __init__(self, dateipfad=None):
        if dateipfad is None:
            home = Path.home()
            app_dir = home / ".wetter_app"
            app_dir.mkdir(exist_ok=True)
            self.dateipfad = app_dir / "favoriten.json"
        else:
            self.dateipfad = Path(dateipfad)
        self.favoriten = []
        self.lade_favoriten()    

    def lade_favoriten(self):
        if os.path.exists(self.dateipfad):
            with open(self.dateipfad, "r", encoding="utf-8") as f:
                try:
                    self.favoriten = json.load(f)
                except json.JSONDecodeError:
                    self.favoriten = []
        else:
            self.favoriten = []

    def speichere_favoriten(self):
        with open(self.dateipfad, "w", encoding="utf-8") as f:
            json.dump(self.favoriten, f, ensure_ascii=False, indent=4)

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
