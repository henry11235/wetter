"""
Wetter App - A weather application.
"""

from .wetter import (
    Wettertyp,
    wetter_beschreibung,
    ort_zu_koordinaten,
    aktuelles_wetter_anzeigen,
    wetter_vorhersage_anzeigen,
    main
)
from .FavoritenManager import FavoritenManager

__all__ = [
    "Wettertyp",
    "wetter_beschreibung",
    "ort_zu_koordinaten",
    "aktuelles_wetter_anzeigen",
    "wetter_vorhersage_anzeigen",
    "FavoritenManager",
    "main"
]
