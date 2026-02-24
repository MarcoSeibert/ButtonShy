import random

from start_up import check_for_assets
from Classes.base.apps import StartApp

if __name__ == "__main__":
    # random.seed(23)
    check_for_assets()

    app_start = StartApp()
    app_start.mainloop()

# todo Goldener Rahmen um aktive Karte
# todo Fenster am Anfang (evtl schon mit Leicht/Normal/Schwer)
# Todo das Ende muss passen
# Todo Fenster am Ende (inkl. restart, zurück ins Menü, Quit)
# Todo Punkte in json speichern für Statistik
# todo Tests: Für alle 18 Karten + Blöcke: einfache Fälle, komplexe Fälle, Randfälle, 2-3 komplette Spiele für alle 18 Karten (vielleicht auch nur 10 Karten?)
# Done: Test für functions.py Todo 18 Karten
# Todo cut cards to better match roads
