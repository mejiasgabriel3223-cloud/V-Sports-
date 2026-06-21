import os
import sys

from engine import Engine
from core.managers.game_scanner import GameScanner


def main():
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(root_dir)
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        print("Iniciando V-Sports Launcher...")

        scanner = GameScanner()
        found_games = scanner.get_games_metadata()

        launcher = Engine(found_games)
        launcher.run()

    except Exception as e:
        import traceback

        print(f"Error crítico: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
