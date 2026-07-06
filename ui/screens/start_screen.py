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
        screen.fill(Settings.BACKGROUND_COLOR)

        if os.path.exists(Settings.MAIN_TITLE_IMAGE):
            title_image = pygame.image.load(Settings.MAIN_TITLE_IMAGE)
            try:
                title_image = title_image.convert_alpha()
            except pygame.error:
                pass
            image_width = min(800, title_image.get_width())
            image_height = int(title_image.get_height() * image_width / title_image.get_width())
            title_image_scaled = pygame.transform.smoothscale(title_image, (image_width, image_height))
            screen.blit(title_image_scaled, (Settings.S_WIDTH // 2 - title_image_scaled.get_width() // 2, 80))
        else:
            title = self.font_title.render("Bienvenido a V-Sports", True, Settings.HIGHLIGHT_COLOR)
            screen.blit(title, (Settings.S_WIDTH // 2 - title.get_width() // 2, Settings.S_HEIGHT // 2 - 120))

        subtitle = _get_font(32).render("Presiona ENTER para inicializar el launcher", True, Settings.TEXT_COLOR)
        screen.blit(subtitle, (Settings.S_WIDTH // 2 - subtitle.get_width() // 2, Settings.S_HEIGHT // 2 + 140))
