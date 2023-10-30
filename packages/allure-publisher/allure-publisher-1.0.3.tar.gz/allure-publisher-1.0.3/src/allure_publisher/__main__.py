from pathlib import Path
from typing import Optional

import typer

from .collector import collect_files
from .publisher import upload_results
from .validators import validate_path_callback


def main(
        url: str = typer.Argument(
            default=...,
            help='Url приемника allure-report'),
        path: Path = typer.Argument(
            default=Path().resolve() / 'results',
            help='Путь до директории с результатами теста',
            callback=validate_path_callback),
        user: Optional[str] = typer.Option(
            None,
            '--user', '-u',
            help='Имя пользователя'
        ),
        password: Optional[str] = typer.Option(
            None,
            '--password', '-p',
            help='Пароль'
        ),
        trigger_build: bool = typer.Option(
            False,
            '--trigger-build', '-t',
            help='Триггер сборки нового отчета allure-report'
        ),
        rebuild_existing_report: bool = typer.Option(
            False,
            '--rebuild-existing-report', '-r',
            help='Пересобрать текущий отчет'
        )
):
    results = collect_files(path)
    upload_results(
        base_url=url,
        results=results,
        username=user,
        password=password,
        trigger_build=trigger_build,
        rebuild_existing_report=rebuild_existing_report
    )


if __name__ == '__main__':
    typer.run(main)
