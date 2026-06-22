"""Paquete games: exporta clases de juego y una `BaseGame` para heredar.

Se introduce `BaseGame` para proporcionar ganchos comunes y atributos
recomendados (`S_WIDTH`, `S_HEIGHT`, `FPS`/`TICK_RATE`) que el lanzador
forzará para mantener coherencia entre juegos.
"""

from typing import List
from core.settings import Settings


class BaseGame:
    """Clase base para juegos.

    Hereda de `BaseGame` y sobreescribe `update(dt)`, `draw()` y opcionalmente
    `handle_events(events)`. El lanzador puede inyectar la pantalla mediante
    `_inject_context(screen)` y llamará a `_stop_context()` cuando termine la
    sesión.

    Atributos de clase recomendados (opcionales): `S_WIDTH`, `S_HEIGHT`,
    `FPS` o `TICK_RATE`. Estos serán ajustados por el lanzador para coincidir
    con `core.settings.Settings`.
    """

    # Atributos opcionales de resolución / tick — los juegos pueden definirlos.
    # Por defecto toman los valores de `core.settings.Settings` (1280x720, 60fps).
    S_WIDTH = Settings.S_WIDTH
    S_HEIGHT = Settings.S_HEIGHT
    FPS = Settings.FPS
    TICK_RATE = Settings.FPS

    def __init__(self) -> None:
        self.screen = None
        self.running = True
        self._running = True

    def _inject_context(self, screen) -> None:
        """Llamado por el engine para proporcionar la superficie de render."""
        self.screen = screen

    def _stop_context(self) -> None:
        """Hook llamado cuando el engine detiene la sesión del juego."""
        try:
            self.stop()
        except Exception:
            self.running = False
            self._running = False

    def stop(self) -> None:
        """Detiene el juego en ejecución; los juegos deben liberar recursos aquí."""
        self._running = False
        self.running = False

    # Manejadores por defecto — sobrescribir en subclases
    def handle_events(self, events: List) -> None:
        return None

    def update(self, dt: float) -> None:
        return None

    def draw(self) -> None:
        # Sin operación por defecto; las subclases deben usar `self.screen`
        return None


from .carrera_de_obstaculos import CarreraDeObstaculos, GAME_METADATA

__all__ = ["BaseGame", "CarreraDeObstaculos", "GAME_METADATA"]
