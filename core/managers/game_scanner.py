import importlib
import os
import sys
from typing import List


class GameScanner:
    def __init__(self, games_dir: str = "games") -> None:
        self.games_dir = games_dir

    def _import_game_module(self, module_name: str):
        try:
            module_path = f"{self.games_dir}.{module_name}"
            if module_path in sys.modules:
                return importlib.reload(sys.modules[module_path])
            return importlib.import_module(module_path)
        except Exception as exc:
            print(f"No se pudo importar el juego '{module_name}': {exc}")
            return None

    def get_games_metadata(self) -> List[dict]:
        games = []
        if not os.path.isdir(self.games_dir):
            return games

        for filename in sorted(os.listdir(self.games_dir)):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue

            module_name = os.path.splitext(filename)[0]
            module = self._import_game_module(module_name)
            if module is None:
                continue

            metadata = getattr(module, "GAME_METADATA", None)
            game_class = getattr(module, "CarreraDeObstaculos", None) or getattr(module, "GAME_CLASS", None)
            if not metadata or not game_class:
                continue

            games.append(
                {
                    "id": metadata.get("id", module_name),
                    "title": metadata.get("title", module_name),
                    "description": metadata.get("description", ""),
                    "authors": metadata.get("authors", []),
                    "group_number": metadata.get("group_number"),
                    "instance": game_class,
                    "cover_path": metadata.get("cover_path"),
                }
            )

        return games
