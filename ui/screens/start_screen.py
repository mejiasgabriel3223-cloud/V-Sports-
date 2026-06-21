import pygame
from core.settings import Settings


class StartScreen:
    def __init__(self) -> None:
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 32)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "MAIN_MENU"
        return None

    def update(self, dt):
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(Settings.BACKGROUND_COLOR)
        title = self.font_title.render("Bienvenido a V-Sports", True, Settings.HIGHLIGHT_COLOR)
        subtitle = self.font_text.render("Presiona ENTER para abrir el launcher", True, Settings.TEXT_COLOR)

        screen.blit(title, (Settings.S_WIDTH // 2 - title.get_width() // 2, Settings.S_HEIGHT // 2 - 80))
        screen.blit(subtitle, (Settings.S_WIDTH // 2 - subtitle.get_width() // 2, Settings.S_HEIGHT // 2 + 20))
