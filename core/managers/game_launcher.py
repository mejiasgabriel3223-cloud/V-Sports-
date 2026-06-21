from typing import Optional


class GameLauncher:
    def __init__(self) -> None:
        self._active_instance = None

    def start(self, game_data: dict):
        game_class = game_data.get("instance")
        if not game_class:
            return None

        instance = game_class()
        self._active_instance = instance
        return instance

    def stop(self) -> None:
        if self._active_instance and hasattr(self._active_instance, "stop"):
            self._active_instance.stop()
        self._active_instance = None

    @property
    def active_instance(self):
        return self._active_instance
