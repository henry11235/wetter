"""
Main entry point for the Wetter application.
"""
import sys
import os
import customtkinter as ctk
import customtkinter as ctk_image
import requests
import datetime
from PIL import Image, ImageTk
from staticmap import StaticMap, CircleMarker
from wetter.favoriten_manager import favoriten_manager
from wetter.weather_api import ort_zu_koordinaten, aktuelles_wetter_anzeigen, wetter_vorhersage_anzeigen, stunden_vorhersage_anzeigen
from wetter.ui import create_favorite_section, update_background, set_background_image, lade_karte
from wetter.weather_types import wetter_beschreibung

def update_background(canvas, root):
    if not hasattr(root, "bg_image_raw"):
        return
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    resized = root.bg_image_raw.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
    root.bg_image = ImageTk.PhotoImage(resized)
    canvas.delete("all")
    canvas.create_image(0, 0, image=root.bg_image, anchor="nw")
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
    image_path = resource_path("assets/" + image_path)
    root.bg_image_raw = Image.open(image_path)
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
        m = StaticMap(200, 200)
        marker = CircleMarker((lon, lat), 'red', 12)
        m.add_marker(marker)
        image = m.render(zoom=3)
        image = image.resize((200, 200), Image.LANCZOS)
        return ctk_image.CTkImage(light_image=image, dark_image=image, size=(200, 200))
    except Exception as e:
        print(f"Fehler beim Erzeugen der Offline-Karte: {e}")
        return None

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

def ort_suchen():
    ort = ort_eingabe.get()
    if not ort:
        ergebnis_label.configure(text="Bitte einen Ort eingeben.")
        return
    try:
        lat, lon, ort_name = ort_zu_koordinaten(ort)
        aktuelles_wetter_anzeigen(lat, lon, ort_name, ergebnis_label, root, canvas, karten_label)
        wetter_vorhersage_anzeigen(lat, lon, vorhersage_label)
    except Exception as e:
        ergebnis_label.configure(text=f"Fehler bei der Ortssuche: {e}")

def add_to_favorites(ort):
    favoriten_manager.hinzufuegen(ort)
    update_favorites_buttons()

def update_favorites_buttons():

    for widget in favorite_buttons_frame.winfo_children():
        widget.destroy()


    for ort in favoriten_manager.gib_favoriten():
        button = ctk.CTkButton(favorite_buttons_frame, text=ort, command=lambda o=ort: select_favorite(o),
                               corner_radius=10, height=40, width=180,
                               fg_color="lightblue", hover_color="lightseagreen", text_color="black")
        button.pack(fill="x", pady=5)


def select_favorite(ort):
    ort_eingabe.delete(0, ctk.END)
    ort_eingabe.insert(0, ort)
    ort_suchen()

def remove_from_favorites(ort):
    favoriten_manager.entfernen(ort)
    update_favorites_buttons()

def create_favorite_section(master):
    global favorite_buttons_frame
    frame = ctk.CTkFrame(master, width=250, height=550, corner_radius=20, fg_color="gray90")
    frame.pack(side="left", fill="y", padx=10, pady=10)

    fav_label = ctk.CTkLabel(frame, text="⭐Favoriten⭐", font=("Arial", 18, "bold"), text_color="black")
    fav_label.pack(pady=10)

    favorite_buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
    favorite_buttons_frame.pack(fill="both", pady=10)


    add_fav_button = ctk.CTkButton(frame, text="Hinzufügen", command=lambda: add_to_favorites(ort_eingabe.get()),
                                   corner_radius=10, width=180, height=40,
                                   fg_color="lightgreen", hover_color="green", text_color="black")
    add_fav_button.pack(pady=5)


    remove_fav_button = ctk.CTkButton(frame, text="Löschen", command=lambda: remove_from_favorites(ort_eingabe.get()),
                                      corner_radius=10, width=180, height=40,
                                      fg_color="lightcoral", hover_color="red", text_color="black")
    remove_fav_button.pack(pady=5)

    update_favorites_buttons()

def main():
    global root, ort_eingabe, ergebnis_label, vorhersage_label, canvas, favorite_buttons_frame, favoriten_manager, karten_label
    favoriten_manager = favoriten_manager()
    favoriten_manager.lade_favoriten()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Wetter App")
    root.geometry("950x600")

    create_favorite_section(root)

    canvas = ctk.CTkCanvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(master=root)
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    ort_eingabe = ctk.CTkEntry(content_frame, width=300, placeholder_text="Ort eingeben")
    ort_eingabe.pack(pady=(20, 10))
    ort_eingabe.insert(0, "Dresden")

    ort_eingabe.bind("<Return>", lambda event: ort_suchen())

    suchen_button = ctk.CTkButton(content_frame, text="Ort suchen", command=ort_suchen)
    suchen_button.pack(pady=10)

    info_frame = ctk.CTkFrame(content_frame)
    info_frame.pack(pady=10, fill="both")

    ergebnis_label = ctk.CTkLabel(info_frame, text="", justify="left", wraplength=350)
    ergebnis_label.pack(side="left", padx=10)

    karten_label = ctk.CTkLabel(info_frame, text="")
    karten_label.pack(side="right", padx=10)

    vorhersage_label = ctk.CTkLabel(content_frame, text="", justify="left", wraplength=450)
    vorhersage_label.pack(pady=10)

    update_favorites_buttons()

    def on_resize(event):
        update_background(canvas, root)

    root.bind("<Configure>", on_resize)

    ort_suchen()

    stundenansicht_frame = ctk.CTkFrame(root)
    stundenansicht_frame.place(relx=0.5, rely=0.5, anchor="center")

    stunden_label = ctk.CTkLabel(stundenansicht_frame, text="", justify="left", wraplength=500)
    stunden_label.pack(pady=20)

    zurueck_button = ctk.CTkButton(stundenansicht_frame, text="Zurück", command=lambda: zeige_hauptansicht())
    zurueck_button.pack(pady=10)

    stunden_button = ctk.CTkButton(content_frame, text="Stündliche Vorhersage", command=lambda: zeige_stundenansicht())
    stunden_button.pack(pady=10)

    stundenansicht_frame.lower()

    def zeige_stundenansicht():
        ort = ort_eingabe.get()
        if not ort:
            stunden_label.configure(text="Bitte zuerst einen Ort eingeben.")
            return
        try:
            lat, lon, _ = ort_zu_koordinaten(ort)
            stunden_vorhersage_anzeigen(lat, lon, stunden_label)
            content_frame.lower()
            stundenansicht_frame.lift()
        except Exception as e:
            stunden_label.configure(text=f"Fehler: {e}")

    def zeige_hauptansicht():
        stundenansicht_frame.lower()
        content_frame.lift()

    root.mainloop()

if __name__ == "__main__":
    main()

