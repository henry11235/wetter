import tkinter as tk
import requests
import datetime 

def wetter_symbol(code):
    if code == 0:
        return "☀️ Klar"
    elif code in [1, 2, 3]:
        return "🌤️ Teilweise bewölkt"
    elif code in [45, 48]:
        return "🌫️ Nebel"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "🌧️ Regen"
    elif code in [71, 73, 75, 85, 86]:
        return "❄️ Schnee"
    elif code in [95, 96, 99]:
        return "🌩️ Gewitter"
    else:
        return "🌡️ Unbekannt"
def aktuelles_wetter_anzeigen():
    url = ( "https://api.open-meteo.com/v1/forecast"
        "?latitude=51.05&longitude=13.74"
        "&current_weather=true"
        "&timezone=Europe%2FBerlin")
    try:
        response = requests.get(url)
        daten = response.json()

        wetter = daten["current_weather"]
        temperatur = wetter["temperature"]
        wind = wetter["windspeed"]
        zeit = wetter["time"]
        wettercode = wetter["weathercode"]
        symbol = wetter_symbol(wettercode)

        text = (  f"Aktuelles Wetter in Dresden ({zeit}):\n"
            f"Temperatur: {temperatur}°C\n"
            f"Wind: {wind} km/h")
        
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"
        
        ergebnis_label.config(text=text)
    except:
        ergebnis_label.config(text="Fehler beim Abruf der Wetterdaten")
    ergebnis_label.after(600000, aktuelles_wetter_anzeigen)    

def main():
    global ergebnis_label
    root = tk.Tk()
    root.title("Wetter App")
    root.geometry("400x300")
    root.update_idletasks()  
    root.geometry("400x300")  

    ergebnis_label = tk.Label(root, text="Klicken Sie auf 'Aktualisieren'")
    ergebnis_label.pack(pady=20)

    aktualisieren_button = tk.Button(root, text="Aktualisieren", command=aktuelles_wetter_anzeigen)
    aktualisieren_button.pack(pady=10)

    aktuelles_wetter_anzeigen()

    root.mainloop()

if __name__ == "__main__":
    main()
