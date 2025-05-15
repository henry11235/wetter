# Wetter
graphische darstellug um wetterdaten abzurufen
## Installation
1. Stelle sicher, dass Python 3.13 oder höher installiert ist
2. Installiere die Abhängigkeiten mit Poetry:
   ```bash
   poetry install
   ```
## Entwicklung
```bash
poetry shell
pytest
```

## Releases
Um eine neue Version der App zu erstellen:

1. Erstelle einen neuen Git-Tag mit dem Versionsnamen (z.B. v1.0.0):
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions wird automatisch:
   - Die Tests ausführen
   - Die macOS-App bauen
   - Eine GitHub-Release erstellen mit der kompilierten App

3. Die kompilierte App kann dann von der GitHub-Releases-Seite heruntergeladen werden.
