from start_up import show_loading_window
from Classes.base.apps import StartApp

if __name__ == "__main__":
    show_loading_window()

    app_start = StartApp()
    app_start.mainloop()
