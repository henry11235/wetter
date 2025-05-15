"""
UI related functions.
"""

import customtkinter as ctk
from PIL import Image, ImageTk
from staticmap import StaticMap, CircleMarker
from .weather_api import ort_zu_koordinaten, aktuelles_wetter_anzeigen, wetter_vorhersage_anzeigen, stunden_vorhersage_anzeigen

def update_background(canvas, root):
    if not hasattr(root, "bg_image_raw"):
        return
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

def lade_karte(lat, lon):
    try:
        m = StaticMap(200, 200)
        marker = CircleMarker((lon, lat), 'red', 12)
        m.add_marker(marker)
        image = m.render(zoom=3)
        image = image.resize((200, 200), Image.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
    except Exception as e:
        print(f"Fehler beim Erzeugen der Offline-Karte: {e}")
        return None

def create_favorite_section(master, favoriten_manager, ort_eingabe, ort_suchen):
    frame = ctk.CTkFrame(master, width=250, height=550, corner_radius=20, fg_color="gray90")
    frame.pack(side="left", fill="y", padx=10, pady=10)

    fav_label = ctk.CTkLabel(frame, text="⭐Favoriten⭐", font=("Arial", 18, "bold"), text_color="black")
    fav_label.pack(pady=10)

    favorite_buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
    favorite_buttons_frame.pack(fill="both", pady=10)

    def update_favorites_buttons():
        for widget in favorite_buttons_frame.winfo_children():
            widget.destroy()

        for ort in favoriten_manager.gib_favoriten():
            button = ctk.CTkButton(favorite_buttons_frame, text=ort, 
                                 command=lambda o=ort: select_favorite(o),
                                 corner_radius=10, height=40, width=180,
                                 fg_color="lightblue", hover_color="lightseagreen", text_color="black")
            button.pack(fill="x", pady=5)

    def select_favorite(ort):
        ort_eingabe.delete(0, ctk.END)
        ort_eingabe.insert(0, ort)
        ort_suchen()

    def add_to_favorites(ort):
        favoriten_manager.hinzufuegen(ort)
        update_favorites_buttons()

    def remove_from_favorites(ort):
        favoriten_manager.entfernen(ort)
        update_favorites_buttons()

    add_fav_button = ctk.CTkButton(frame, text="Hinzufügen", 
                                 command=lambda: add_to_favorites(ort_eingabe.get()),
                                 corner_radius=10, width=180, height=40,
                                 fg_color="lightgreen", hover_color="green", text_color="black")
    add_fav_button.pack(pady=5)

    remove_fav_button = ctk.CTkButton(frame, text="Löschen", 
                                    command=lambda: remove_from_favorites(ort_eingabe.get()),
                                    corner_radius=10, width=180, height=40,
                                    fg_color="lightcoral", hover_color="red", text_color="black")
    remove_fav_button.pack(pady=5)

    update_favorites_buttons()
    return frame 