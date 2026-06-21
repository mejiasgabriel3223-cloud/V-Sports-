# V-Sports Launcher

Launcher modular inspirado en la estructura de `enfocate` con separación clara de responsabilidades.

## Estructura de archivos

- `main.py`  
  Punto de entrada principal del proyecto. Inicializa el escáner de juegos y arranca el motor.

- `engine.py`  
  Controla el ciclo principal de Pygame: manejo de eventos, actualización, dibujo y cambio de estados.

- `requirements.txt`  
  Dependencias del proyecto.

- `core/settings.py`  
  Configuración global del launcher, resolución fija 1280x720 y FPS 60.

- `core/managers/asset_manager.py`  
  Carga y mantiene assets globales como fuentes y portadas de juegos.

- `core/managers/sound_player.py`  
  Gestión básica de audio para detener y reproducir sonidos.

- `core/managers/game_launcher.py`  
  Abstracción para iniciar y detener instancias de juego.

- `core/managers/game_scanner.py`  
  Escanea y devuelve metadatos de juegos disponibles. Actualmente es un placeholder para integrar más tarde.

- `ui/screens/boot_screen.py`  
  Pantalla de arranque inicial del launcher.

- `ui/screens/main_menu.py`  
  Menú principal que lista juegos y envía la acción de lanzamiento.

- `ui/screens/__init__.py`  
  Exporta los componentes de pantalla para importaciones limpias.

## Cómo usar

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el launcher:
   ```bash
   python main.py
   ```

3. Agrega juegos en `core/managers/game_scanner.py` y, si quieres, registra instancias válidas en `core/managers/game_launcher.py`.

## Notas

- Resolución forzada en `core/settings.py`: `1280x720`.
- El bucle principal usa `Settings.FPS` y `pygame.time.Clock()` para mantener 60 FPS.
- La arquitectura está lista para crecer con más gestores, pantallas e integraciones.
