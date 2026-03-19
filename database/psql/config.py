from __future__ import annotations
import os
from configparser import ConfigParser

def load_config(filename: str = "database.ini", section: str = "postgresql") -> dict[str, str]:
    """Load DB connection parameters from an INI file using absolute paths."""
    
    # 1. Obtenemos la ruta del directorio donde vive ESTE archivo (config.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Construimos la ruta completa hacia el archivo .ini
    path_to_ini = os.path.join(current_dir, filename)

    parser = ConfigParser()
    
    # 3. Verificamos si el archivo existe físicamente
    if not os.path.exists(path_to_ini):
        raise FileNotFoundError(f"No se encontró el archivo de configuración en: {path_to_ini}")

    parser.read(path_to_ini)

    if not parser.has_section(section):
        raise RuntimeError(f"Sección [{section}] no encontrada en {path_to_ini}")

    return {k: v for k, v in parser.items(section)}