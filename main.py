import os
import sys

from core.managers.game_scanner import GameScanner
from launcher import Launcher


def main():
    try:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        os.chdir(ROOT_DIR)
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)

        print("Iniciando V-Sports Launcher...")

        games_folder = os.path.join(ROOT_DIR, "games")
        found_games = GameScanner.scan_and_load_metadata(games_folder)

        #Se pasa al launcher el catalogo y la ruta
        launcher = Launcher(found_games=found_games, games_path=games_folder)
        launcher.run()

    except Exception as e:
        import traceback

        print(f"Error crítico: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
