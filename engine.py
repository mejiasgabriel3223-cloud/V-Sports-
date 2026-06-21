import pygame
from core.settings import Settings
from core.managers.asset_manager import AssetManager
from core.managers.game_launcher import GameLauncher
from core.managers.sound_player import SoundPlayer
from ui.screens import BootScreen, MainMenu, StartScreen


class Engine:
    def __init__(self, found_games):
        pygame.init()

        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.music.stop()

        pygame.display.set_caption(Settings.TITLE)
        self.screen = pygame.display.set_mode((Settings.S_WIDTH, Settings.S_HEIGHT))
        self.clock = pygame.time.Clock()

        AssetManager.load_all_assets()
        AssetManager.load_game_covers(found_games)

        self.games_list = found_games
        self.launcher_manager = GameLauncher()
        self.active_game = None

        self.screens = {
            "BOOT": BootScreen(),
            "START": StartScreen(),
            "MAIN_MENU": MainMenu(self.games_list),
        }

        self.current_state = "START"
        self.running = True

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12 and self.current_state == "IN_GAME":
                    if self.active_game:
                        pygame.mouse.set_visible(True)
                        self.active_game._stop_context()

        if self.current_state == "IN_GAME" and self.active_game:
            if hasattr(self.active_game, "estado_actual") and self.active_game.estado_actual == "MENU":
                for event in events:
                    pygame.event.post(event)
            else:
                if hasattr(self.active_game, "handle_events"):
                    self.active_game.handle_events(events)
        else:
            result = self.screens[self.current_state].handle_events(events)
            if result:
                self._process_screen_result(result)

    def _process_screen_result(self, result):
        if result == "QUIT":
            self.running = False
        elif isinstance(result, dict) and result.get("action") == "LAUNCH":
            self._start_game_session(result.get("game_data"))
        elif result in self.screens:
            self.current_state = result

    def update(self, dt):
        if self.current_state == "IN_GAME" and self.active_game:
            try:
                self.active_game.update(dt)
                active_running = getattr(self.active_game, "_running", None)
                if active_running is None:
                    active_running = getattr(self.active_game, "running", True)
                if not active_running:
                    self._reset_to_menu()
            except Exception as e:
                print(f"Error: {e}")
                self._reset_to_menu()
            return

        result = self.screens[self.current_state].update(dt)

        if result:
            if result == "QUIT":
                self.running = False
            elif isinstance(result, dict) and result.get("action") == "LAUNCH":
                self._start_game_session(result.get("game_data"))
            elif result in self.screens:
                self.current_state = result

    def _start_game_session(self, game_data):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        instance = self.launcher_manager.start(game_data)

        if instance:
            if hasattr(instance, "_inject_context"):
                instance._inject_context(self.screen)
            self.active_game = instance
            self.current_state = "IN_GAME"
        else:
            print(f"Fail: {game_data.get('title')}")

    def _reset_to_menu(self):
        if self.active_game:
            if hasattr(self.active_game, "_stop_context"):
                self.active_game._stop_context()
            self.launcher_manager.stop()

            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

            SoundPlayer.stop_all()

            pygame.mouse.set_visible(True)

            self.active_game = None
            self.current_state = "MAIN_MENU"
            self.screen = pygame.display.set_mode((Settings.S_WIDTH, Settings.S_HEIGHT))
            pygame.display.set_caption(Settings.TITLE)
            SoundPlayer.play_music("menu")

    def draw(self):
        if self.current_state == "IN_GAME" and self.active_game:
            self.active_game.draw()
        else:
            self.screens[self.current_state].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(Settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
