from typing import Optional
from core.settings import Settings


class GameLauncher:
    def __init__(self) -> None:
        self._active_instance = None

    def start(self, game_data: dict):
        game_class = game_data.get("instance")
        if not game_class:
            return None

        instance = game_class()

        # Forzar resolución y tick/FPS para que coincidan con `Settings` del motor.
        desired_w = Settings.S_WIDTH
        desired_h = Settings.S_HEIGHT
        desired_fps = Settings.FPS

        attr_map = [
            ("S_WIDTH", desired_w),
            ("S_HEIGHT", desired_h),
            ("TICK_RATE", desired_fps),
            ("FPS", desired_fps),
        ]

        resolution_forced = False
        fps_forced = False

        for attr, desired in attr_map:
            try:
                if hasattr(instance, attr):
                    orig = getattr(instance, attr)
                    if orig != desired:
                        setattr(instance, attr, desired)
                        print(f"Ajustado {attr} de {orig} -> {desired} en {game_class.__name__}")
                        if attr in ("S_WIDTH", "S_HEIGHT"):
                            resolution_forced = True
                        if attr in ("FPS", "TICK_RATE"):
                            fps_forced = True
                else:
                    # Si el atributo no existe, lo creamos con el valor forzado
                    setattr(instance, attr, desired)
                    print(f"Establecido {attr} = {desired} en {game_class.__name__} (no existía)")
                    if attr in ("S_WIDTH", "S_HEIGHT"):
                        resolution_forced = True
                    if attr in ("FPS", "TICK_RATE"):
                        fps_forced = True
            except Exception as e:
                print(f"No se pudo ajustar {attr} en {game_class.__name__}: {e}")

        if resolution_forced or fps_forced:
            print(
                f"Se forzaron parámetros de visualización en {game_class.__name__}: "
                f"resolución {desired_w}x{desired_h}, FPS {desired_fps}"
            )

        self._active_instance = instance
        return instance

    def stop(self) -> None:
        if self._active_instance and hasattr(self._active_instance, "stop"):
            self._active_instance.stop()
        self._active_instance = None

    @property
    def active_instance(self):
        return self._active_instance
