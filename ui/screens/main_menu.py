import pygame
from typing import List

from core.managers.asset_manager import AssetManager
from core.settings import Settings


def _get_font(size: int) -> pygame.font.Font:
    if hasattr(AssetManager, "get_font"):
        return AssetManager.get_font(size)
    return pygame.font.Font(None, size)


class MainMenu:
    def __init__(self, games_list: List[dict]) -> None:
        self.games_list = list(games_list)
        self.selected_index = 0
        self.quit_button_rect = pygame.Rect(Settings.S_WIDTH - 140, 20, 120, 40)
        self.menu_top = 120
        self.row_height = 60
        self.visible_rows = max(1, (Settings.S_HEIGHT - 260) // self.row_height)
        self.scroll_offset = 0

    def _render_multiline(self, screen, text, font, color, x, y, max_width, line_height):
        words = text.split()
        line = ""
        for word in words:
            test_line = (line + " " + word).strip()
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                screen.blit(font.render(line, True, color), (x, y))
                y += line_height
                line = word
        if line:
            screen.blit(font.render(line, True, color), (x, y))
            y += line_height
        return y

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                    self._ensure_selection_visible()
                elif event.key == pygame.K_DOWN:
                    self.selected_index = min(len(self.games_list) - 1, self.selected_index + 1)
                    self._ensure_selection_visible()
                elif event.key == pygame.K_RETURN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.quit_button_rect.collidepoint(mouse_pos):
                        return "QUIT"
                    
                    # CORRECCIÓN: Volvemos a poner la lógica para lanzar el juego
                    if self.games_list:
                        selected = self.games_list[self.selected_index]
                        if selected.get("ghost"):
                            return None
                        return {"action": "LAUNCH", "game_data": selected}
                        
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.quit_button_rect.collidepoint(event.pos):
                    return "QUIT"
        return None

    def _ensure_selection_visible(self):
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.visible_rows:
            self.scroll_offset = self.selected_index - self.visible_rows + 1

    def update(self, dt):
        return None

    def draw(self, screen: pygame.Surface) -> None:
        background = AssetManager.get_asset("menu_background")
        if background:
            screen.blit(pygame.transform.scale(background, (Settings.S_WIDTH, Settings.S_HEIGHT)), (0, 0))
        else:
            screen.fill(Settings.BACKGROUND_COLOR)

        list_panel_rect = pygame.Rect(40, self.menu_top - 20, 620, self.visible_rows * self.row_height + 60)
        pygame.draw.rect(screen, (25, 25, 25), list_panel_rect, border_radius=18)
        pygame.draw.rect(screen, Settings.HIGHLIGHT_COLOR, list_panel_rect, 2, border_radius=18)

        title_label_font = _get_font(30)
        title_label = title_label_font.render("Juegos", True, (255, 255, 255))
        screen.blit(title_label, (list_panel_rect.x + 24, list_panel_rect.y - 36))

        details_panel_rect = pygame.Rect(Settings.S_WIDTH - 440, 100, 420, 560)
        pygame.draw.rect(screen, (25, 25, 25), details_panel_rect, border_radius=18)
        pygame.draw.rect(screen, Settings.HIGHLIGHT_COLOR, details_panel_rect, 2, border_radius=18)

        details_content_rect = pygame.Rect(details_panel_rect.x + 18, details_panel_rect.y + 18, details_panel_rect.width - 36, details_panel_rect.height - 36)
        pygame.draw.rect(screen, (35, 35, 35), details_content_rect, border_radius=16)

        font = _get_font(28)

        visible_end = min(self.scroll_offset + self.visible_rows, len(self.games_list))
        for index in range(self.scroll_offset, visible_end):
            game = self.games_list[index]
            label = f"> {game.get('title', 'Juego sin nombre')}" if index == self.selected_index else game.get('title', 'Juego sin nombre')
            color = Settings.HIGHLIGHT_COLOR if index == self.selected_index else Settings.TEXT_COLOR
            y = self.menu_top + (index - self.scroll_offset) * self.row_height
            if index == self.selected_index:
                row_rect = pygame.Rect(60, y - 4, 560, self.row_height - 8)
                pygame.draw.rect(screen, (45, 45, 45), row_rect, border_radius=12)
            text = font.render(label, True, color)
            screen.blit(text, (80, y))

        pygame.draw.rect(screen, (220, 50, 50), self.quit_button_rect)
        pygame.draw.rect(screen, Settings.HIGHLIGHT_COLOR, self.quit_button_rect, 2)
        quit_text = font.render("Salir", True, (255, 255, 255))
        screen.blit(
            quit_text,
            (
                self.quit_button_rect.x + self.quit_button_rect.width // 2 - quit_text.get_width() // 2,
                self.quit_button_rect.y + self.quit_button_rect.height // 2 - quit_text.get_height() // 2,
            ),
        )

        # CORRECCIÓN: Verificamos que haya juegos y declaramos 'selected' antes de sacar su info
        if self.games_list:
            selected = self.games_list[self.selected_index]
            
            title_text = selected.get("title", "")
            description = selected.get("description", "")
            authors = selected.get("authors", [])
            group = selected.get("group_number", "")

            cover = AssetManager.get_cover(selected.get("id", ""))
            cover = pygame.transform.scale(cover, (380, 260))
            cover_x = Settings.S_WIDTH - 420
            cover_y = 120
            cover_card_rect = pygame.Rect(cover_x - 6, cover_y - 6, 392, 272)
            pygame.draw.rect(screen, (10, 10, 10), cover_card_rect, border_radius=20)
            pygame.draw.rect(screen, Settings.HIGHLIGHT_COLOR, cover_card_rect, 2, border_radius=20)
            screen.blit(cover, (cover_x, cover_y))
            pygame.draw.rect(screen, Settings.HIGHLIGHT_COLOR, (cover_x, cover_y, 380, 260), 2, border_radius=18)

            info_x = cover_x
            info_y = cover_y + 280
            title_font = pygame.font.Font(None, 40)
            text_font = _get_font(20)

            screen.blit(title_font.render(title_text, True, Settings.HIGHLIGHT_COLOR), (info_x, info_y))
            info_y += 44
            info_y = self._render_multiline(screen, description, text_font, Settings.TEXT_COLOR, info_x, info_y, 360, 26)
            info_y += 8
            screen.blit(text_font.render("Autores:", True, Settings.TEXT_COLOR), (info_x, info_y))
            info_y += 32
            screen.blit(text_font.render(", ".join(authors), True, Settings.TEXT_COLOR), (info_x, info_y))
            info_y += 40
            screen.blit(text_font.render(f"Grupo: {group}", True, Settings.TEXT_COLOR), (info_x, info_y))

        hint_font = _get_font(20)
        hint = hint_font.render("Flechas ARRIBA/ABAJO para cambiar de juego", True, Settings.TEXT_COLOR)
        screen.blit(hint, (80, Settings.S_HEIGHT - 80))