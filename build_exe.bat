@echo off
REM Build-Skript für deine Wetter-App .exe
pyinstaller --onefile --add-data "assets;assets" run.py
