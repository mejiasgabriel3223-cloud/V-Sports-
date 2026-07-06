import pygame

from core.managers.asset_manager import AssetManager
from core.settings import Settings


class StartScreen:
    def __init__(self) -> None:
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = AssetManager.get_font(32)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "MAIN_MENU"
        return None

    def update(self, dt):
        return None

    def draw(self, screen: pygame.Surface) -> None:
        background = AssetManager.get_asset("menu_background")
        if background:
            screen.blit(pygame.transform.scale(background, (Settings.S_WIDTH, Settings.S_HEIGHT)), (0, 0))
        else:
            screen.fill(Settings.BACKGROUND_COLOR)

        title_image = AssetManager.get_asset("main_title_image")
        if title_image:
            image_width = min(800, title_image.get_width())
            image_height = int(title_image.get_height() * image_width / title_image.get_width())
            title_image_scaled = pygame.transform.smoothscale(title_image, (image_width, image_height))
            screen.blit(title_image_scaled, (Settings.S_WIDTH // 2 - title_image_scaled.get_width() // 2, 80))
        else:
            title = self.font_title.render("Bienvenido a V-Sports", True, Settings.HIGHLIGHT_COLOR)
            screen.blit(title, (Settings.S_WIDTH // 2 - title.get_width() // 2, Settings.S_HEIGHT // 2 - 120))

        subtitle = AssetManager.get_font(32).render("Presiona ENTER para abrir el launcher", True, Settings.TEXT_COLOR)
        screen.blit(subtitle, (Settings.S_WIDTH // 2 - subtitle.get_width() // 2, Settings.S_HEIGHT // 2 + 140))
