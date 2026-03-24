import os
from typing import TYPE_CHECKING
import pytest

from conftest import make_request_with_retry, get_request

if TYPE_CHECKING:
    from nomad.client import Auth


@pytest.mark.parametrize(
    "app",
    [pytest.param(app, id=app.get("path", "<no-path>")) for app in make_request_with_retry(get_request, "apps/entry-points", auth=None).json().get("data", [])],
)
def test_app_entry_point(auth: "Auth", app):
    """Each app entry point should respond successfully."""
    app_path = app.get("path")
    if not app_path:
        pytest.skip(f"App without path: {app}")

    apps_to_skip = [
        p.strip()
        for p in os.environ.get("APP_ENTRY_POINTS_TO_SKIP", "").split(",")
        if p.strip()
    ]
    if app_path in apps_to_skip:
        pytest.skip(f"App '{app_path}' is in APP_ENTRY_POINTS_TO_SKIP")

    detail_url = f"apps/entry-points/{app_path}"
    resp = make_request_with_retry(get_request, detail_url, auth, check_status=False)
    assert resp.status_code == 200, f"App '{app_path}' failed: {resp.text}"
