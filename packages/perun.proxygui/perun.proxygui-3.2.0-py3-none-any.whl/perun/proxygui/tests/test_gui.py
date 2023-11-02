import re
import tempfile
from unittest.mock import patch

import pytest
from flask_session import Session

from perun.proxygui.app import get_flask_app
from perun.proxygui.tests.shared_test_data import (
    SHARED_TESTING_CONFIG,
    OIDCAuthenticationMock,
)
from perun.utils.ConfigStore import ConfigStore

MOCK_SESSIONS = [
    ("client_1", "session_id_1", "issuer_1"),
    ("client_2", "session_id_2", "issuer_2"),
]
MOCK_SERVICE_NAMES = {"client_1": {"en": "Client 1"}, "client_2": {"en": "Client 2"}}
MOCK_SERVICES_CONFIG = {
    "RPS": {"client_1": {"FRONTCHANNEL_LOGOUT": {"LOGOUT_URI": "/test_logout_uri"}}}
}


@pytest.fixture()
def client():
    with patch(
        "perun.utils.ConfigStore.ConfigStore.get_global_cfg",
        return_value=SHARED_TESTING_CONFIG,
    ), patch(
        "perun.utils.ConfigStore.ConfigStore.get_attributes_map",
        return_value=SHARED_TESTING_CONFIG,
    ), patch(
        "perun.proxygui.app.init_oidc_rp_handler",
        return_value=None,
    ), patch(
        "perun.proxygui.app.get_oidc_auth",
        return_value=OIDCAuthenticationMock(),
    ), patch(
        "perun.proxygui.logout_manager.LogoutManager.fetch_services_configuration",
        return_value=MOCK_SERVICES_CONFIG,
    ):
        cfg = ConfigStore.get_config()
        app = get_flask_app(cfg)
        app.config["TESTING"] = True

        app.config["SESSION_TYPE"] = "filesystem"
        with tempfile.TemporaryDirectory() as temp_session_folder:
            app.config["SESSION_FILE_DIR"] = temp_session_folder
        Session(app)

        yield app.test_client()


def test_is_testing_sp(client):
    response = client.get("/IsTestingSP")
    is_testing_sp_text = (
        "You are about to access service, which is in testing environment."
        # noqa
    )
    is_testing_sp_text_2 = "Continue"

    result = response.data.decode()
    assert is_testing_sp_text in result
    assert is_testing_sp_text_2 in result
    assert response.status_code == 200


def test_authorization_error(client):
    response = client.get("/authorization")

    assert response.status_code == 404


@patch("perun.proxygui.jwt.JWTService.verify_jwt")
def test_authorization(mock_method, client):
    test_data = {
        "email": "email",
        "service": "service",
        "registration_url": "url",
    }

    is_testing_sp_text = "Access forbidden"
    is_testing_sp_text_2 = (
        "You don't meet the prerequisites for accessing the service: "  # noqa
    )
    is_testing_sp_text_3 = (
        "For more information about this service please visit this "  # noqa
    )
    is_testing_sp_text_4 = (
        "If you think you should have an access contact service operator at "
        # noqa
    )
    is_testing_sp_text_5 = "Problem with login to service: "
    mock_method.return_value = test_data
    response = client.get("/authorization/example")

    result = response.data.decode()
    assert is_testing_sp_text in result
    assert is_testing_sp_text_2 in result
    assert is_testing_sp_text_3 in result
    assert is_testing_sp_text_4 in result
    assert is_testing_sp_text_5 in result
    assert response.status_code == 200


def test_sp_authorization_error(client):
    response = client.get("/SPAuthorization")

    assert response.status_code == 404


def test_logout_cookies_missing(client):
    response = client.get("/logout")
    result = response.data.decode()
    cookies_missing = "cookies are missing"
    assert cookies_missing in result


def test_logout_overview(client):
    with patch(
        "perun.proxygui.user_manager.UserManager._get_ssp_session_by_key",
        return_value={"user": 123},
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_active_client_ids_for_user",
        return_value=MOCK_SESSIONS,
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_active_client_ids_for_session",
        return_value=[MOCK_SESSIONS[0]],
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_all_rp_names",
        return_value=MOCK_SERVICE_NAMES,
    ):
        client.set_cookie(key="SimpleSAMLSessionID", value="123456")
        response = client.get("/logout")
        result = response.data.decode()
        session_services, device_services = result.split("on your other devices")
        assert "Client 1" in session_services
        assert "Client 2" not in session_services
        assert "Client 1" in device_services
        assert "Client 2" in device_services


def test_logout_state_wrong_flow(client):
    client.set_cookie(key="SimpleSAMLSessionID", value="123456")
    response = client.get("/logout_state", follow_redirects=False)
    redirected_url = response.headers["Location"]
    assert redirected_url.endswith("/logout")


def test_logout_state_iframe(client):
    with patch(
        "perun.proxygui.user_manager.UserManager._get_ssp_session_by_key",
        return_value={"user": 123},
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_active_client_ids_for_user",
        return_value=MOCK_SESSIONS,
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_active_client_ids_for_session",
        return_value=[MOCK_SESSIONS[0]],
    ), patch(
        "perun.proxygui.user_manager.UserManager.get_all_rp_names",
        return_value=MOCK_SERVICE_NAMES,
    ), patch(
        "perun.proxygui.user_manager.UserManager.logout",
        return_value=None,
    ), patch(
        "perun.proxygui.user_manager.UserManager.sub_to_user_id", return_value="1"
    ):
        client.set_cookie(key="SimpleSAMLSessionID", value="123456")
        with client.session_transaction() as session:
            session["logout_params"] = {}
            session["init_logged_out_service"] = {}
        response = client.get("/logout_state", follow_redirects=True)
        iframe_pattern = re.compile(r'<iframe.*?src="/test_logout_uri".*?</iframe>')
        assert iframe_pattern.search(response.text) is not None


@patch("perun.proxygui.jwt.JWTService.verify_jwt")
def test_sp_authorization(mock_method, client):
    test_data = {
        "email": "mail",
        "service": "service",
        "registration_url": "url",
    }
    is_testing_sp_text = "You are not authorized to access the service "
    is_testing_sp_text_2 = (
        "We will now redirect you to a registration page, "
        + "where you will apply for the access."
    )
    is_testing_sp_text_3 = "Proceed to registration"
    mock_method.return_value = test_data
    response = client.get("/SPAuthorization/example")

    result = response.data.decode()
    assert is_testing_sp_text in result
    assert is_testing_sp_text_2 in result
    assert is_testing_sp_text_3 in result
    assert response.status_code == 200
