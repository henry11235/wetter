import customtkinter as ctk
import requests
import datetime
from PIL import Image, ImageTk
import json
import os
import io
import enum

# --- KONSTANTEN ---
LOCATIONIQ_API_KEY = "pk.8785e94e9f62466f4bf7350354c541eb"  # <-- Hier deinen API-Key eintragen

class FavoritenManager:
    def __init__(self, dateipfad="favoriten.json"):
        self.dateipfad = dateipfad
        self.favoriten = []
        self.lade_favoriten()

    def lade_favoriten(self):
        if os.path.exists(self.dateipfad):
            try:
                with open(self.dateipfad, "r") as f:
                    self.favoriten = json.load(f)
            except Exception as e:
                print(f"Fehler beim Laden der Favoriten: {e}")
                self.favoriten = []

    def speichere_favoriten(self):
        try:
            with open(self.dateipfad, "w") as f:
                json.dump(self.favoriten, f)
        except Exception as e:
            print(f"Fehler beim Speichern der Favoriten: {e}")

    def hinzufuegen(self, ort):
        if ort and ort not in self.favoriten:
            self.favoriten.append(ort)
            self.speichere_favoriten()

    def entfernen(self, ort):
        if ort in self.favoriten:
            self.favoriten.remove(ort)
            self.speichere_favoriten()

    def gib_favoriten(self):
        return self.favoriten

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

def update_background(canvas, root):
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    resized = root.bg_image_raw.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    root.bg_image = ImageTk.PhotoImage(resized)
    canvas.delete("all")
    canvas.create_image(0, 0, image=root.bg_image, anchor="nw")

def set_background_image(weather_code, root, canvas):
    image_map = {
        0: "sonnig.jpg",
        1: "wolkig.jpg", 2: "wolkig.jpg", 3: "wolkig.jpg",
        45: "nebel.jpg", 48: "nebel.jpg",
        51: "regen.jpg", 53: "regen.jpg", 55: "regen.jpg", 61: "regen.jpg", 63: "regen.jpg", 65: "regen.jpg", 80: "regen.jpg", 81: "regen.jpg", 82: "regen.jpg",
        71: "schnee.jpg", 73: "schnee.jpg", 75: "schnee.jpg", 85: "schnee.jpg", 86: "schnee.jpg",
        95: "gewitter.jpg", 96: "gewitter.jpg", 99: "gewitter.jpg"
    }
    image_path = image_map.get(weather_code)
    if not image_path:
        return
    root.bg_image_raw = Image.open("src/wetter/assets/" + image_path)
    update_background(canvas, root)

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

def lade_karte(lat, lon):
    try:
        url = f"https://maps.locationiq.com/v3/staticmap?key={LOCATIONIQ_API_KEY}&center={lat},{lon}&zoom=12&size=200x200&markers=icon:small-red-cutout|{lat},{lon}"
        response = requests.get(url)
        response.raise_for_status()
        image_data = io.BytesIO(response.content)
        return ImageTk.PhotoImage(Image.open(image_data))
    except Exception as e:
        print(f"Fehler beim Abrufen der Karte: {e}")
        return None

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

        text = (f"Aktuelles Wetter in {ort_name} ({zeit}):\n"
                f"{symbol}\n"
                f"Temperatur: {temperatur}°C\n"
                f"Wind: {wind} km/h")
        zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y – %H:%M:%S")
        text += f"\nZuletzt aktualisiert: {zeitstempel}"

        ergebnis_label.configure(text=text)
        set_background_image(wettercode, root, canvas)

        # Karte anzeigen
        karte = lade_karte(lat, lon)
        if karte:
            karten_label.configure(image=karte)
            karten_label.image = karte

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
    favoriten_manager.hinzufuegen(ort)
    update_favorites_buttons()

def update_favorites_buttons():
    for widget in favorite_buttons_frame.winfo_children():
        widget.destroy()
    for ort in favoriten_manager.gib_favoriten():
        button = ctk.CTkButton(favorite_buttons_frame, text=ort, command=lambda o=ort: select_favorite(o))
        button.pack(fill="x", pady=2)

def select_favorite(ort):
    ort_eingabe.delete(0, ctk.END)
    ort_eingabe.insert(0, ort)
    ort_suchen()

def remove_from_favorites(ort):
    favoriten_manager.entfernen(ort)
    update_favorites_buttons()

def create_favorite_section(master):
    global favorite_buttons_frame
    frame = ctk.CTkFrame(master, width=200, height=600, fg_color="lightblue")
    frame.pack(side="left", fill="y", padx=10, pady=10)

    fav_label = ctk.CTkLabel(frame, text="Favoriten", font=("Arial", 16))
    fav_label.pack(pady=10)

    favorite_buttons_frame = ctk.CTkFrame(frame, width=180, height=400)
    favorite_buttons_frame.pack(fill="both", pady=10)

    add_fav_button = ctk.CTkButton(frame, text="Hinzufügen", command=lambda: add_to_favorites(ort_eingabe.get()))
    add_fav_button.pack(pady=10)

    remove_fav_button = ctk.CTkButton(frame, text="Löschen", command=lambda: remove_from_favorites(ort_eingabe.get()))
    remove_fav_button.pack(pady=10)

def main():
    global root, ort_eingabe, ergebnis_label, vorhersage_label, canvas, favorite_buttons_frame, favoriten_manager, karten_label
    favoriten_manager = FavoritenManager()

    root = ctk.CTk()
    root.title("Wetter App")
    root.geometry("900x600")

    create_favorite_section(root)

    canvas = ctk.CTkCanvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(master=root, fg_color="lightblue")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Ort-Eingabe und Button
    ort_eingabe = ctk.CTkEntry(content_frame, width=300, placeholder_text="Ort eingeben")
    ort_eingabe.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=10)
    ort_eingabe.insert(0, "Dresden")

    suchen_button = ctk.CTkButton(content_frame, text="Ort suchen", command=ort_suchen)
    suchen_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Wettertext (links) und Karte (rechts)
    ergebnis_label = ctk.CTkLabel(content_frame, text="", justify="left", wraplength=350)
    ergebnis_label.grid(row=2, column=0, sticky="nw", padx=10, pady=10)

    karten_label = ctk.CTkLabel(content_frame, text="")
    karten_label.grid(row=2, column=1, sticky="ne", padx=10, pady=10)

    # Vorhersage (unterhalb)
    vorhersage_label = ctk.CTkLabel(content_frame, text="", justify="left", wraplength=700)
    vorhersage_label.grid(row=3, column=0, columnspan=2, pady=10)

    update_favorites_buttons()

    def on_resize(event):
        if hasattr(root, "bg_image_raw"):
            update_background(canvas, root)

    root.bind("<Configure>", on_resize)

    ort_suchen()
    root.mainloop()

if __name__ == "__main__":
    main()
