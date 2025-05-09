import tkinter as tk
import requests

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

        text = (  f"Aktuelles Wetter in Dresden ({zeit}):\n"
            f"Temperatur: {temperatur}°C\n"
            f"Wind: {wind} km/h")
        
        ergebnis_label.config(text=text)
    except:
        ergebnis_label.config(text="Fehler beim Abruf der Wetterdaten")

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

    root.mainloop()

if __name__ == "__main__":
    main()
