import os
import json


class GameScanner:
    """Explora la carpeta de juegos y construye un catálogo con sus metadatos."""

    @staticmethod
    def scan_and_load_metadata(base_path: str):
        """
        Escanea el directorio de juegos, detecta proyectos que contienen un main.py
        y convierte su metadata.json en un diccionario listo para mostrar en el menú.
        """
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        catalog = []

        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)

            # Un juego se considera válido si existe como carpeta y contiene un archivo main.py.
            if os.path.isdir(folder_path) and "main.py" in os.listdir(folder_path):
                json_path = os.path.join(folder_path, "metadata.json")

                # Metadatos base por si el juego no define todos los campos.
                metadata = {
                    "folder": folder,
                    "folder_path": folder_path,
                    "title": folder.replace("_", " "),
                    "description": "No se encontró descripción en metadata.json",
                    "authors": "Desconocido",
                    "group_number": "Desconocido",
                    "controls": "No fueron especificados los controles en metadata.json",
                }

                if os.path.exists(json_path):
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            group_data = json.load(f)
                            metadata.update(group_data)
                    except Exception as e:
                        print(f"Error al leer el archivo metadata.json en la carpeta '{folder}': {e}")

                catalog.append(metadata)

        return catalog
        