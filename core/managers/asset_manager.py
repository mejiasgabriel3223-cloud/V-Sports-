import os
from typing import Dict, List, Optional

import pygame

from core.settings import Settings


class AssetManager:
    _assets: Dict[str, object] = {}
    _covers: Dict[str, pygame.Surface] = {}
    _font_path: Optional[str] = None

    @classmethod
    def load_all_assets(cls) -> None:
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        cls._font_path = Settings.FONT_PATH if os.path.exists(Settings.FONT_PATH) else None
        if cls._font_path:
            cls._assets["font"] = pygame.font.Font(cls._font_path, 36)
        else:
            cls._assets["font"] = pygame.font.Font(None, 36)

        if os.path.exists(Settings.MENU_BACKGROUND_IMAGE):
            background = pygame.image.load(Settings.MENU_BACKGROUND_IMAGE)
            try:
                if pygame.display.get_init() and pygame.display.get_surface():
                    background = background.convert()
            except pygame.error:
                pass
            cls._assets["menu_background"] = pygame.transform.scale(background, (Settings.S_WIDTH, Settings.S_HEIGHT))
        if os.path.exists(Settings.MAIN_TITLE_IMAGE):
            title_image = pygame.image.load(Settings.MAIN_TITLE_IMAGE)
            try:
                title_image = title_image.convert_alpha()
            except pygame.error:
                pass
            max_width = min(800, title_image.get_width())
            image_height = int(title_image.get_height() * max_width / title_image.get_width())
            cls._assets["main_title_image"] = pygame.transform.smoothscale(title_image, (max_width, image_height))

    @classmethod
    def load_game_covers(cls, games: List[dict]) -> None:
        for game in games:
            game_folder_path = game.get("folder_path")
            if game_folder_path and os.path.exists(game_folder_path):
                cover_path = os.path.join(game_folder_path, "assets", "cover") #El cover del juego debe estar en una carpeta cover dentro de assets
                
                if os.path.exists(cover_path):
                    cls._covers[game["folder"]] = pygame.image.load(cover_path).convert_alpha()
                    continue

                alt_path = cls._find_cover_alternative(cover_path) if cover_path else None
                if alt_path:
                    cls._covers[game["folder"]] = pygame.image.load(alt_path).convert_alpha()
                    continue

                cls._covers[game["folder"]] = pygame.Surface((200, 120))
                cls._covers[game["folder"]].fill((32, 48, 72))

    @classmethod
    def _find_cover_alternative(cls, cover_path: Optional[str]) -> Optional[str]:
        if not cover_path:
            return None

        base, _ = os.path.splitext(cover_path)
        for ext in [".png", ".jpg", ".jpeg"]:
            alt_path = f"{base}{ext}"
            if os.path.exists(alt_path):
                return alt_path
        return None

    @classmethod
    def get_asset(cls, name: str):
        return cls._assets.get(name)

    @classmethod
    def get_font(cls, size: int) -> pygame.font.Font:
        if cls._font_path and os.path.exists(cls._font_path):
            return pygame.font.Font(cls._font_path, size)
        return pygame.font.Font(None, size)

    @classmethod
    def get_cover(cls, folder: str) -> pygame.Surface:
        return cls._covers.get(folder, pygame.Surface((200, 120)))
