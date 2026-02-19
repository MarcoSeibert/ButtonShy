import random

from start_up import check_for_assets
from Classes.base.apps import StartApp

if __name__ == "__main__":
    random.seed(1)
    check_for_assets()

    app_start = StartApp()
    app_start.mainloop()
