import tkinter as tk
import requests
import datetime 
from PIL import Image, ImageTk
import os 

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

def set_background_image(weather_code, root, canvas):
    if weather_code == 0:
        image_path = "sonnig.jpg"
    elif weather_code in [1, 2, 3]:
        image_path = "bewoelkt.jpg"
    elif weather_code in [45, 48]:
        image_path = "nebel.jpg"
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        image_path = "regen.jpg"
    elif weather_code in [71, 73, 75, 85, 86]:
        image_path = "schnee.jpg"
    elif weather_code in [95, 96, 99]:
        image_path = "gewitter.jpg"
    else:
        print("Bild nicht gefunden")  
        return 

    bg_image_raw = Image.open("src/wetter/" + image_path)
    bg_image_raw = bg_image_raw.resize((600, 400), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image_raw)
    
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    root.bg_image = bg_image 
    
def ort_zu_koordinaten(ort):
    
    url = f"https://nominatim.openstreetmap.org/search?q={ort}&format=json&limit=1"
    try:
        response = requests.get(url, headers={"User-Agent": "wetter-app"})
        daten = response.json()
        if daten:
            lat = float(daten[0]["lat"])
            lon = float(daten[0]["lon"])
            name = daten[0]["display_name"].split(",")[0]  
            return lat, lon, name
        else:
            raise ValueError("Ort nicht gefunden")
    except Exception as e:
        raise e     

def aktuelles_wetter_anzeigen(lat, lon, ort_name):
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
        symbol = wetter_symbol(wettercode)

        text =  (f"Aktuelles Wetter in Dresden ({zeit}):\n"
            f"{symbol}\n"
            f"Temperatur: {temperatur}°C\n"
            f"Wind: {wind} km/h")
        
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"

        ergebnis_label.config(text=text)
        set_background_image(wettercode, root, canvas)

    except Exception as e:
        ergebnis_label.config(text=f"Fehler beim Abruf der Wetterdaten: {e}")
        
def wetter_vorhersage_anzeigen(lat, lon):
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
            symbol = wetter_symbol(codes[i])
            vorhersage_text += f"{datum}: {symbol} {min_temp[i]}–{max_temp[i]}°C\n"

        vorhersage_label.config(text=vorhersage_text)

    except Exception as e:
        vorhersage_label.config(text=f"Fehler bei der Vorhersage: {e}")
        
def ort_suchen():
   
    ort = ort_eingabe.get()
    if not ort:
        ergebnis_label.config(text="Bitte einen Ort eingeben.")
        return
    try:
        lat, lon, ort_name = ort_zu_koordinaten(ort)
        aktuelles_wetter_anzeigen(lat, lon, ort_name)
        wetter_vorhersage_anzeigen(lat, lon)
    except Exception as e:
        ergebnis_label.config(text=f"Fehler bei der Ortssuche: {e}")
        
             
        
def main():
    global ergebnis_label, root, canvas, vorhersage_label, ort_eingabe

    root = tk.Tk()
    root.title("Wetter App")
    root.geometry("600x400")

    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack(fill="both", expand=True)

    titel_label = tk.Label(root, text="Wetter App", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#00796b")
    canvas.create_window(300, 40, window=titel_label)
    
    ort_eingabe = tk.Entry(root, font=("Arial", 14))  
    ort_eingabe.insert(0, "Dresden")  
    canvas.create_window(300, 80, window=ort_eingabe)

    
    ergebnis_label = tk.Label(root, text="Lade Wetterdaten...", font=("Arial", 16), bg="#e0f7fa", fg="#004d40")
    canvas.create_window(300, 150, window=ergebnis_label)
    
    global vorhersage_label
    vorhersage_label = tk.Label(root, text="", font=("Arial", 14), bg="#e0f7fa", fg="#004d40")
    canvas.create_window(300, 220, window=vorhersage_label)
    
    
    aktualisieren_button = tk.Button(
    root, text="Ort suchen", command=ort_suchen,
    font=("Arial", 14), bg="#004d40", fg="black", activebackground="grey"
    )
    canvas.create_window(300, 300, window=aktualisieren_button)


    ort_suchen()
    root.mainloop()

if __name__ == "__main__":
    main()
