"""
Utilidades para manejo de archivos:
- Renombrar archivos en batch (minusculas, sin espacios)
- Listar archivos por extension
- Mover archivos segun patron
"""

import os
import re
from pathlib import Path


def normalize_filename(name: str) -> str:
    """Convierte nombre a minusculas, reemplaza espacios y caracteres especiales."""
    name = name.lower()
    name = re.sub(r'[áàâã]', 'a', name)
    name = re.sub(r'[éèê]',  'e', name)
    name = re.sub(r'[íìî]',  'i', name)
    name = re.sub(r'[óòôõ]', 'o', name)
    name = re.sub(r'[úùû]',  'u', name)
    name = re.sub(r'[ñ]',    'n', name)
    name = re.sub(r'[^a-z0-9.\-_]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name


def batch_rename(folder: str, dry_run: bool = True) -> list[tuple[str, str]]:
    """Renombra todos los archivos de una carpeta normalizando sus nombres."""
    folder_path = Path(folder)
    changes = []

    for file in folder_path.iterdir():
        if file.is_file():
            new_name = normalize_filename(file.name)
            if new_name != file.name:
                changes.append((file.name, new_name))
                if not dry_run:
                    file.rename(folder_path / new_name)

    return changes


def list_by_extension(folder: str, ext: str) -> list[str]:
    """Lista todos los archivos con una extension especifica."""
    return [f.name for f in Path(folder).glob(f'**/*.{ext}')]


if __name__ == '__main__':
    # Ejemplo de uso
    folder = '.'
    changes = batch_rename(folder, dry_run=True)
    for old, new in changes:
        print(f'{old} -> {new}')
