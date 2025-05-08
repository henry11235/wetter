import tkinter as tk
from wetter import root

def test_window_title():
    assert root.title() == "Wetter App"

def test_window_geometry():
    geometry = root.geometry().split('+')[0]  # Get just the size part (e.g., "400x300")
    assert geometry == "400x300" 