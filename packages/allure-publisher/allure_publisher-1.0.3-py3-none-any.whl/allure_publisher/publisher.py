import sys
from typing import Optional, IO
from uuid import uuid4

import httpx


def upload_results(
        base_url: str,
        results: IO[bytes],
        trigger_build: bool = False,
        rebuild_existing_report: bool = False,
        username: Optional[str] = None,
        password: Optional[str] = None
):
    """Загрузить результаты в приемник allure-report"""
    if username and password:
        auth = httpx.BasicAuth(username, password)
    else:
        auth = None

    with httpx.Client(base_url=base_url, auth=auth, timeout=httpx.Timeout(60)) as client:
        response = client.post(
            url='/results/upload',
            files={'file': (str(uuid4()), results)},
            data={
                'trigger_build': trigger_build,
                'rebuild_existing_report': rebuild_existing_report
            }
        )

        if not response.is_success:
            sys.exit(response.text)

        print(response.text)
