import os
import pygame

from core.managers.asset_manager import AssetManager
from core.settings import Settings


def _get_font(size: int) -> pygame.font.Font:
    if hasattr(AssetManager, "get_font"):
        return AssetManager.get_font(size)
    return pygame.font.Font(None, size)


class StartScreen:
    def __init__(self) -> None:
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = _get_font(32)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "MAIN_MENU"
        return None

    def update(self, dt):
        return None

    def draw(self, screen: pygame.Surface) -> None:
        # Use the MAIN_TITLE_IMAGE as a full-screen background/title
        if os.path.exists(Settings.MAIN_TITLE_IMAGE):
            try:
                bg = pygame.image.load(Settings.MAIN_TITLE_IMAGE)
                try:
                    bg = bg.convert_alpha()
                except pygame.error:
                    pass
                bg_scaled = pygame.transform.smoothscale(bg, (Settings.S_WIDTH, Settings.S_HEIGHT))
                screen.blit(bg_scaled, (0, 0))
            except Exception:
                screen.fill(Settings.BACKGROUND_COLOR)
        else:
            screen.fill(Settings.BACKGROUND_COLOR)

        # Subtitle prompt over the background
        subtitle = _get_font(32).render("Presiona ENTER para inicializar el launcher", True, Settings.TEXT_COLOR)
        screen.blit(subtitle, (Settings.S_WIDTH // 2 - subtitle.get_width() // 2, Settings.S_HEIGHT // 2 + 140))
