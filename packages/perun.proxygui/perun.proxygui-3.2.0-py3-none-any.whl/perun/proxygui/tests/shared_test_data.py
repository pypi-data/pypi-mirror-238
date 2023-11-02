import functools
from unittest.mock import patch

import pytest

from perun.proxygui.app import get_flask_app
from perun.utils.ConfigStore import ConfigStore

SHARED_TESTING_CONFIG = {
    "adapters_manager": {"adapters": {}},
    "attrs_cfg_path": "mock_path",
    "perun_person_principal_names_attribute": "mock_name",
}
ATTRS_MAP = {}


def mock_passthrough_decorator(*args, **kwargs):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            return view_func(*args, **kwargs)

        return wrapper

    return decorator


class OIDCAuthenticationMock:
    """
    Acts as a pass-through class to bypass OIDC authentication wrapper when testing
    other functionality.
    """

    def oidc_auth(self, _: str):
        return mock_passthrough_decorator()


@pytest.fixture()
def client():
    with patch(
        "perun.utils.ConfigStore.ConfigStore.get_global_cfg",
        return_value=SHARED_TESTING_CONFIG,
    ), patch(
        "perun.utils.ConfigStore.ConfigStore.get_attributes_map",
        return_value=ATTRS_MAP,
    ), patch(
        "perun.proxygui.app.init_oidc_rp_handler",
        return_value=None,
    ), patch(
        "perun.proxygui.app.get_oidc_auth",
        return_value=OIDCAuthenticationMock(),
    ), patch(
        "perun.proxygui.logout_manager.LogoutManager.__init__", return_value=None
    ):
        cfg = ConfigStore.get_config()
        app = get_flask_app(cfg)
        app.config["TESTING"] = True
        yield app.test_client()
