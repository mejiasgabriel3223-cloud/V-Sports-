import pygame


class SoundPlayer:
    @staticmethod
    def stop_all() -> None:
        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.music.stop()

    @staticmethod
    def play_music(track_name: str) -> None:
        if not pygame.mixer.get_init():
            return
        # placeholder para música de menú
        pygame.mixer.music.stop()

    @staticmethod
    def play_sound(sound) -> None:
        if not pygame.mixer.get_init():
            return
        sound.play()
