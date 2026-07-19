# V-Sports Launcher

V-Sports Launcher es una interfaz centralizada para descubrir, mostrar y ejecutar juegos desde un mismo entorno. El proyecto está pensado como un lanzador modular: el menú presenta los juegos disponibles, el motor se encarga de iniciar cada uno en su propia ventana y el sistema de assets gestiona los recursos visuales y de audio.

## Qué hace el launcher

El flujo general del programa es el siguiente:

1. El archivo principal inicia la aplicación.
2. El escáner busca juegos dentro de la carpeta de juegos del proyecto.
3. El menú lee ese catálogo y muestra información como título, descripción, autores y portada.
4. Cuando el usuario selecciona un juego, el motor lo lanza como un subproceso independiente.
5. Al volver, el launcher reinicia su interfaz y reanuda la música del menú.

## Cómo funciona internamente

- main.py
  Es el punto de entrada del proyecto. Ajusta la ruta raíz, prepara el entorno y crea una instancia del launcher.

- launcher.py
  Coordina la interfaz del launcher, el estado actual de pantalla y la solicitud de ejecución del juego seleccionado.

- engine.py
  Se encarga de abrir el juego elegido como proceso independiente. Esto permite que cada juego corra en su propia ventana sin mezclar su ciclo de ejecución con el del launcher.

- core/managers/game_scanner.py
  Recorre la carpeta de juegos y construye un catálogo con los metadatos de cada proyecto.

- core/managers/asset_manager.py
  Carga fuentes, fondos y portadas para que el menú se vea correctamente.

- core/managers/sound_player.py
  Gestiona la música y el audio del launcher.

- ui/screens/
  Contiene las pantallas del launcher: arranque, bienvenida y menú principal.

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

Y ejecuta el proyecto con:

```bash
python main.py
```

## Cómo agregar juegos

Por ahora, el launcher detecta los juegos que existen dentro de la carpeta games del proyecto. Para añadir uno nuevo, sigue estos pasos:

1. Crea una carpeta nueva dentro de games con el nombre del juego.
2. Añade un archivo main.py dentro de esa carpeta. Ese archivo será el punto de entrada del juego.
3. Añade un archivo metadata.json con la información del juego. La estructura mínima puede ser:

```json
{
  "title": "Mi Juego",
  "description": "Descripción breve del juego",
  "authors": ["Autor 1", "Autor 2"],
  "group_number": 1,
  "controls": "Teclas de movimiento"
}
```

4. Coloca la portada del juego en la ruta:

```text
games/<nombre_del_juego>/assets/cover/launcher_cover
```

El launcher intentará cargar esa imagen como portada. Si no existe, usará una portada genérica.

5. Asegúrate de que la carpeta del juego contenga un main.py. Sin ese archivo, no será detectada por el escáner.

## Formato esperado para los juegos

Para que un juego sea compatible con el launcher, es recomendable que:

- tenga un archivo main.py como punto de entrada;
- incluya un metadata.json con información básica;
- use la carpeta assets/cover/launcher_cover para la portada si quieres que se vea en el menú;
- esté preparado para ejecutarse de forma independiente, ya que el launcher lo abrirá en un subproceso.

## Ejemplo incluido: Carrera de Obstáculos

El proyecto ya incluye un juego compatible dentro de la carpeta games: Carrera de Obstáculos del Grupo 7 del Jueves como ejemplo. Sirve como referencia para ver cómo debe organizarse un juego nuevo.

Su estructura básica es la siguiente:

```text
games/
└── Carrera_de_Obstaculos/
    ├── main.py
    ├── metadata.json
    ├── entities.py
    ├── game.py
    ├── menu.py
    └── assets/
        └── cover/
```

Este ejemplo muestra cómo un juego puede tener:

- un archivo main.py como punto de entrada;
- un metadata.json para los datos que muestra el launcher;
- módulos adicionales como entities.py, game.py y menu.py para separar la lógica;
- una carpeta assets/cover para la portada utilizada en el menú.

## Futuro: lectura directa desde el repositorio

La versión actual escanea la carpeta local games del proyecto. En una actualización futura, el sistema podrá leer los juegos directamente desde el repositorio remoto o desde una ruta de origen configurable.

Eso implicará dos mejoras principales:

- el escáner ya no dependerá únicamente de la carpeta local del proyecto;
- el launcher podrá mostrar juegos disponibles en el repositorio sin necesidad de copiarlos manualmente a la carpeta local.

En esa futura implementación, la lógica de detección seguirá siendo similar: se identificará cada juego por su carpeta, su archivo main.py y su metadata.json, pero la fuente de datos será el repositorio en lugar del directorio local.

## Notas técnicas

- La resolución base del launcher es 1280x720 y el FPS objetivo es 60.
- El menú usa el catálogo generado por el escáner para mostrar los juegos.
- El motor lanza cada juego como un proceso independiente para mantener la interfaz principal estable.
