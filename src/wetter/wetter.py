import customtkinter as ctk
import requests
import datetime
from PIL import Image, ImageTk

favoriten = []

def wetter_beschreibung(code):
    if code == 0:
        return "Sonnig ☀️"
    elif code in [1, 2, 3]:
        return "Bewölkt ☁️"
    elif code in [45, 48]:
        return "Nebel 🌫️"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "Regen 🌧️"
    elif code in [71, 73, 75, 85, 86]:
        return "Schnee 🌨️"
    elif code in [95, 96, 99]:
        return "Gewitter ⛈️"
    else:
        return "Unbekannt"

def update_background(canvas, root):
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    resized = root.bg_image_raw.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    root.bg_image = ImageTk.PhotoImage(resized)
    canvas.delete("all")  
    canvas.create_image(0, 0, image=root.bg_image, anchor="nw")

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

    root.bg_image_raw = Image.open("src/wetter/" + image_path)
    update_background(canvas, root)

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
        symbol = wetter_beschreibung(wettercode)

        text =  (f"Aktuelles Wetter in {ort_name} ({zeit}):\n"
            f"{symbol}\n"
            f"Temperatur: {temperatur}°C\n"
            f"Wind: {wind} km/h")
        
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"

        ergebnis_label.configure(text=text)
        set_background_image(wettercode, root, canvas)
    except Exception as e:
        ergebnis_label.configure(text=f"Fehler beim Abruf der Wetterdaten: {e}")

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
            symbol = wetter_beschreibung(codes[i])
            vorhersage_text += f"{datum}: {symbol} {min_temp[i]}–{max_temp[i]}°C\n"

        vorhersage_label.configure(text=vorhersage_text)

    except Exception as e:
        vorhersage_label.configure(text=f"Fehler bei der Vorhersage: {e}")

def ort_suchen():
    ort = ort_eingabe.get()
    if not ort:
        ergebnis_label.configure(text="Bitte einen Ort eingeben.")
        return
    try:
        lat, lon, ort_name = ort_zu_koordinaten(ort)
        aktuelles_wetter_anzeigen(lat, lon, ort_name)
        wetter_vorhersage_anzeigen(lat, lon)
    except Exception as e:
        ergebnis_label.configure(text=f"Fehler bei der Ortssuche: {e}")

def add_to_favorites(ort):
    if ort and ort not in favoriten:
        favoriten.append(ort)
        update_favorites_buttons()

def update_favorites_buttons():
    for widget in favorite_buttons_frame.winfo_children():
        widget.destroy()  # Löscht bestehende Buttons
    for ort in favoriten:
        button = ctk.CTkButton(favorite_buttons_frame, text=ort, command=lambda o=ort: select_favorite(o))
        button.pack(fill="x", pady=2)

def select_favorite(ort):
    ort_eingabe.delete(0, ctk.END)
    ort_eingabe.insert(0, ort)
    ort_suchen()

def create_favorite_section(master):
    global favorite_buttons_frame
    frame = ctk.CTkFrame(master, width=200, height=600, fg_color="lightgray")
    frame.pack(side="left", fill="y", padx=10, pady=10)
    
    # Titel für Favoriten
    fav_label = ctk.CTkLabel(frame, text="Favoriten", font=("Arial", 16))
    fav_label.pack(pady=10)

    favorite_buttons_frame = ctk.CTkFrame(frame, width=180, height=400)
    favorite_buttons_frame.pack(fill="both", pady=10)
    
    # Favoriten hinzufügen
    add_fav_button = ctk.CTkButton(frame, text="Hinzufügen", command=lambda: add_to_favorites(ort_eingabe.get()))
    add_fav_button.pack(pady=10)

def main():
    global root, ort_eingabe, ergebnis_label, vorhersage_label, background_label, canvas

    root = ctk.CTk()
    root.title("Wetter App")
    root.geometry("800x600")

    create_favorite_section(root)

    canvas = ctk.CTkCanvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(master=root, width=500, height=350, fg_color="transparent")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    ort_eingabe = ctk.CTkEntry(content_frame, width=300, placeholder_text="Ort eingeben")
    ort_eingabe.pack(pady=(20, 10))
    ort_eingabe.insert(0, "Dresden")

    suchen_button = ctk.CTkButton(content_frame, text="Ort suchen", command=ort_suchen)
    suchen_button.pack(pady=10)

    ergebnis_label = ctk.CTkLabel(content_frame, text="", justify="left", wraplength=450)
    ergebnis_label.pack(pady=10)

    vorhersage_label = ctk.CTkLabel(content_frame, text="", justify="left", wraplength=450)
    vorhersage_label.pack(pady=10)

    def on_resize(event):
        if hasattr(root, "bg_image_raw"):
            update_background(canvas, root)

    root.bind("<Configure>", on_resize)

    ort_suchen()
    root.mainloop()

if __name__ == "__main__":
    main()


