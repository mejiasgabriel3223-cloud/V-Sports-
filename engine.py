import os
import sys
import pygame
import subprocess

class Engine:
    def __init__(self, games_path):
        self.GAMES_FOLDER = games_path


    def launch_game(self, game_data):
        """
        Gestiona el ciclo de apagado de pantalla del launcher e invoca el juego.
        El flujo se detiene aqui hasta que se cierre la ventana del juego
        """
        folder = game_data["folder"]
        title = game_data["title"]

        #Construimos las rutas universales utilizando el directorio inyectado
        main_path = os.path.join(self.GAMES_FOLDER, folder, "main.py")
        working_directory = os.path.dirname(main_path)

        print(f"Apagando el launcher para inicializar el juego '{title}'")

        #Apagamos la ventana del launcher, y pausamos el audio
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()
        
        pygame.display.quit()
        
        try:
            #Lanza la ventana independiente. Si hay errores de ejecucion saltaran en su propia ventana de terminal
            self._invoke_game_subprocess(main_path, working_directory)
            return True
        except Exception as e:
            print(f"Error critico de sistema al ejecutar subproceso: {e}")
            return False
        finally:
            print(f"Reinicializando el launcher")

            pygame.display.init()

            if pygame.mixer.get_init():
                pygame.mixer.music.unpause
            
            #Vaciamos la cola de eventos al regresar del juego
            pygame.event.clear()

    def _invoke_game_subprocess(self, main_path, working_directory):
        "Abre una ventana de comandos independiente segun el sistema operativo"
        "para ejecutar el juego solicitado de forma aislada como subproceso"
        
        #MANEJO DE SUBPORCESOS MULTIPLATAFORMA

        #Windows, usa la api nativa para duplicar y abrir consolas independientes
        if sys.platform == "win32":
            subprocess.run(
                [sys.executable, main_path],
                cwd=working_directory,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        #Caso para MacOS o Linux, se ejecuta el proceso de python directamente en el hilo actual del launcher
        #Por falta de api nativa para creacion de una terminal nueva que congele los procesos del launcher
        else:
            subprocess.run(
                [sys.executable, main_path],
                cwd=working_directory
            )
            