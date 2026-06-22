# V-Sports Launcher

Launcher modular para ejecutar juegos en un entorno común, con separación clara de responsabilidades.

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

## Cómo crear juegos compatibles

Sigue estas recomendaciones para que un juego sea reconocido y gestionado por el launcher:

- Heredar de `BaseGame` (exportado desde el paquete `games`) o seguir su contrato: implementar los métodos `update(dt)`, `draw()` y opcionalmente `handle_events(events)`.
- Definir metadatos en el módulo: `GAME_METADATA` con claves mínimas: `id`, `title`, `description`, `authors`, `group_number`, `cover_path`.
- Exportar la clase del juego con el nombre del juego o `GAME_CLASS` (el escáner busca `CarreraDeObstaculos` o `GAME_CLASS`).
- No controles de resolución o reloj dentro del juego: use `self.screen` (inyectada por `_inject_context(screen)`) para dibujar y confíe en `Settings`/`Engine` para el `FPS`.
- Recomendado: declarar atributos de clase opcionales `S_WIDTH`, `S_HEIGHT`, `FPS` si desea documentar expectativas; el `GameLauncher` fuerza estos valores a los de `core.settings.Settings`.
- Evitar constantes de módulo `SCREEN_W`/`SCREEN_H`; use `self.S_WIDTH`/`self.S_HEIGHT`.

Ejemplo mínimo:

```python
from games import BaseGame

GAME_METADATA = {
  'id': 'mi_juego',
  'title': 'Mi Juego',
  'description': 'Descripción breve',
  'authors': ['Autor'],
  'group_number': 1,
  'cover_path': 'assets/covers/mi_juego.png',
}

class MiJuego(BaseGame):
  def __init__(self):
    super().__init__()
    # usar self.S_WIDTH / self.S_HEIGHT

  def handle_events(self, events):
    pass

  def update(self, dt):
    pass

  def draw(self):
    if self.screen:
      # dibujar en self.screen
      pass
```

Con esto el launcher podrá detectar, ajustar parámetros y ejecutar tu juego de forma coherente.
