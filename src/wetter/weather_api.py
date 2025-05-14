"""
Weather API related functions.
"""

import requests
import datetime
from .weather_types import wetter_beschreibung

def ort_zu_koordinaten(ort):
    url = f"https://nominatim.openstreetmap.org/search?q={ort}&format=json&limit=1"
    response = requests.get(url, headers={"User-Agent": "wetter-app"})
    daten = response.json()
    if daten:
        lat = float(daten[0]["lat"])
        lon = float(daten[0]["lon"])
        name = daten[0]["display_name"].split(",")[0]
        return lat, lon, name
    raise ValueError("Ort nicht gefunden")

def aktuelles_wetter_anzeigen(lat, lon, ort_name, ergebnis_label, root, canvas, karten_label):
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}"
           "&current_weather=true"
           "&timezone=Europe%2FBerlin")
    try:
        response = requests.get(url)
        response.raise_for_status()
        daten = response.json()

        wetter = daten["current_weather"]
        temperatur = wetter["temperature"]
        wind = wetter["windspeed"]
        zeit = wetter["time"]
        wettercode = wetter["weathercode"]
        symbol = wetter_beschreibung(wettercode)

        text = (f"Aktuelles Wetter in {ort_name} ({zeit}):\n"
                f"{symbol}\n"
                f"Temperatur: {temperatur}°C\n"
                f"Wind: {wind} km/h")
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"

        ergebnis_label.configure(text=text)
        set_background_image(wettercode, root, canvas)

        karte = lade_karte(lat, lon)
        if karte:
            karten_label.configure(image=karte, text="")
            karten_label.image = karte

    except Exception as e:
        ergebnis_label.configure(text=f"Fehler beim Abruf der Wetterdaten: {e}")

def wetter_vorhersage_anzeigen(lat, lon, vorhersage_label):
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}"
           "&daily=temperature_2m_max,temperature_2m_min,weathercode"
           "&timezone=Europe%2FBerlin")
    try:
        response = requests.get(url)
        response.raise_for_status()
        daten = response.json()

        tage = daten["daily"]["time"]
        max_temp = daten["daily"]["temperature_2m_max"]
        min_temp = daten["daily"]["temperature_2m_min"]
        codes = daten["daily"]["weathercode"]

        vorhersage_text = "3-Tage-Vorhersage:\n"
        for i in range(3):
            datum = datetime.datetime.strptime(tage[i], "%Y-%m-%d").strftime("%A, %d.%m.")
            symbol = wetter_beschreibung(codes[i])
            vorhersage_text += f"{datum}: {symbol} {min_temp[i]}–{max_temp[i]}°C\n"

        vorhersage_label.configure(text=vorhersage_text)

    except Exception as e:
        vorhersage_label.configure(text=f"Fehler bei der Vorhersage: {e}")

def stunden_vorhersage_anzeigen(lat, lon, stunden_label):
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}"
           "&hourly=temperature_2m,weathercode"
           "&timezone=Europe%2FBerlin")
    try:
        response = requests.get(url)
        response.raise_for_status()
        daten = response.json()

        stunden = daten["hourly"]["time"]
        temperaturen = daten["hourly"]["temperature_2m"]
        codes = daten["hourly"]["weathercode"]

        jetzt = datetime.datetime.now()
        vorhersage_text = "Stündliche Vorhersage:\n\n"

        for i in range(len(stunden)):
            zeitpunkt = datetime.datetime.strptime(stunden[i], "%Y-%m-%dT%H:%M")
            if zeitpunkt > jetzt and zeitpunkt < jetzt + datetime.timedelta(hours=12):
                uhrzeit = zeitpunkt.strftime("%H:%M")
                symbol = wetter_beschreibung(codes[i])
                vorhersage_text += f"{uhrzeit}: {symbol}, {temperaturen[i]}°C\n"

        stunden_label.configure(text=vorhersage_text)

    except Exception as e:
        stunden_label.configure(text=f"Fehler beim Abruf: {e}") 