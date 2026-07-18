import pygame
from core.settings import Settings
from core.managers.asset_manager import AssetManager

from core.managers.sound_player import SoundPlayer
from ui.screens import BootScreen, MainMenu, StartScreen

from engine import Engine


class Launcher:
    def __init__(self, found_games, games_path):
        pygame.init()

        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.music.stop()

        pygame.display.set_caption(Settings.TITLE)
        self.screen = pygame.display.set_mode((Settings.S_WIDTH, Settings.S_HEIGHT))
        self.clock = pygame.time.Clock()

        AssetManager.load_all_assets()
        AssetManager.load_game_covers(found_games)

        self.menu_music_path = SoundPlayer.play_music()

        #Fuardamos el catalogo de juegos y la ruta inyectada
        self.games_list = found_games
        self.GAMES_FOLDER = games_path

        #El launcher inicializa el motor de ejecución de juegos
        self.engine = Engine(self.GAMES_FOLDER)


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

        else:
            result = self.screens[self.current_state].handle_events(events)
            if result:
                self._process_screen_result(result)

    def _process_screen_result(self, result):
        if result == "QUIT":
            self.running = False
        elif isinstance(result, dict) and result.get("action") == "LAUNCH":
            self._request_game_start(result.get("game_data"))
        elif result in self.screens:
            self.current_state = result

    def update(self, dt):
        result = self.screens[self.current_state].update(dt)

        if result:
            if result == "QUIT":
                self.running = False
            elif isinstance(result, dict) and result.get("action") == "LAUNCH":
                self._request_game_start(result.get("game_data"))
            elif result in self.screens:
                self.current_state = result

    def _request_game_start(self, game_data):
        """Solicita al motor que ejecute el juego, y al volver reinicia los procesos del launcher de ser necesario"""
        self.engine.launch_game(game_data)
        
        #Al volver del juego:
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        SoundPlayer.stop_all()
        pygame.mouse.set_visible(True)

        self.current_state = "MAIN_MENU"
        self.screen = pygame.display.set_mode((Settings.S_WIDTH, Settings.S_HEIGHT))
        pygame.display.set_caption(Settings.TITLE)
        if self.menu_music_path:
            SoundPlayer.play_music(self.menu_music_path)
        else:
            SoundPlayer.play_music()

    def draw(self):
        self.screens[self.current_state].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(Settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
