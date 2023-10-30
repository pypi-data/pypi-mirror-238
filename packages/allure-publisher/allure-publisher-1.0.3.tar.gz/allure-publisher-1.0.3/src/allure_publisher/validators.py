from pathlib import Path

import typer


def validate_path_callback(value: Path):
    if not value.is_dir():
        raise typer.BadParameter(f'{value} не является директорией')
    return value
