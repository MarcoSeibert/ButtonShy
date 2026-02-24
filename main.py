from Classes.base.apps import StartApp
from start_up import check_for_assets

if __name__ == "__main__":
    check_for_assets()

    app_start = StartApp()
    app_start.mainloop()

# Todo Fenster am Ende (inkl. restart, zurück ins Menü, Quit)
# Todo Punkte in json speichern für Statistik
# y todo Tests: Für alle 18 Karten + Blöcke: einfache Fälle, komplexe Fälle, Randfälle, 2-3 komplette Spiele für alle 18 Karten (vielleicht auch nur 10 Karten?)
# Done: Test für functions.py Todo 18 Karten
# Todo difficulty
