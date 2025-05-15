"""
Weather types and related functions.
"""

import enum

class Wettertyp(enum.Enum):
    SONNIG = "Sonnig ☀️"
    BEOEWOLKT = "Bewölkt ☁️"
    NEBEL = "Nebel 🌫️"
    REGEN = "Regen 🌧️"
    SCHNEE = "Schnee 🌨️"
    GEWITTER = "Gewitter ⛈️"
    UNBEKANNT = "Unbekannt"

def wetter_beschreibung(code):
    if code == 0:
        return Wettertyp.SONNIG.value
    elif code in [1, 2, 3]:
        return Wettertyp.BEOEWOLKT.value
    elif code in [45, 48]:
        return Wettertyp.NEBEL.value
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return Wettertyp.REGEN.value
    elif code in [71, 73, 75, 85, 86]:
        return Wettertyp.SCHNEE.value
    elif code in [95, 96, 99]:
        return Wettertyp.GEWITTER.value
    else:
        return Wettertyp.UNBEKANNT.value 