import os
from typing import Dict, List, Optional

import pygame

from core.settings import Settings


class AssetManager:
    _assets: Dict[str, pygame.Surface] = {}
    _covers: Dict[str, pygame.Surface] = {}

    @classmethod
    def load_all_assets(cls) -> None:
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        cls._assets = {
            "font": pygame.font.Font(None, 36),
        }

    @classmethod
    def load_game_covers(cls, games: List[dict]) -> None:
        for game in games:
            cover_path = game.get("cover_path")
            if cover_path and os.path.exists(cover_path):
                cls._covers[game["id"]] = pygame.image.load(cover_path).convert_alpha()
                continue

            alt_path = cls._find_cover_alternative(cover_path) if cover_path else None
            if alt_path:
                cls._covers[game["id"]] = pygame.image.load(alt_path).convert_alpha()
                continue

            cls._covers[game["id"]] = pygame.Surface((200, 120))
            cls._covers[game["id"]].fill((32, 48, 72))

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
    def get_cover(cls, game_id: str) -> pygame.Surface:
        return cls._covers.get(game_id, pygame.Surface((200, 120)))
