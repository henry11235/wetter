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
        
root = tk.Tk()
root.title("Wetter App")
root.geometry("400x300")
root.update_idletasks()  
root.geometry("400x300")  

if __name__ == "__main__":
    root.mainloop()
