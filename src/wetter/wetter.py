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
    url = ("https://api.open-meteo.com/v1/forecast"
        "?latitude=51.05&longitude=13.74"
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
        symbol = wetter_symbol(wettercode)

        text =  (f"Aktuelles Wetter in Dresden ({zeit}):\n"
            f"{symbol}\n"
            f"Temperatur: {temperatur}°C\n"
            f"Wind: {wind} km/h")
        
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"

        ergebnis_label.config(text=text)
        
    except requests.exceptions.RequestException as e:
        ergebnis_label.config(text=f"Fehler beim Abruf der Wetterdaten: {e}")
    except KeyError:
        ergebnis_label.config(text="Fehler beim Verarbeiten der Wetterdaten")
    except Exception as e:
        ergebnis_label.config(text=f"Ein unerwarteter Fehler ist aufgetreten: {e}")    
    
def main():
    global ergebnis_label
    root = tk.Tk()
    root.title("Wetter App")
    root.geometry("400x300")
    root.configure(bg="#f0f8ff")
    root.update_idletasks()
    root.geometry("400x300")

    ergebnis_label = tk.Label(root, text="Lade Wetterdaten...", font=("Arial", 14), justify="left", bg="#f0f8ff", fg="blue", padx=20, pady=10)
    ergebnis_label.pack(pady=20)

    aktualisieren_button = tk.Button(root, text="Aktualisieren", command=aktuelles_wetter_anzeigen, font=("Arial", 12), bg="#4CAF50", fg="black", padx=10, pady=5)
    aktualisieren_button.pack(pady=10)

    aktuelles_wetter_anzeigen()

    root.mainloop()

if __name__ == "__main__":
    main()
