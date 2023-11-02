import uuid

import requests

from perun.proxygui.jwt import SingletonJWTServiceProvider
from perun.utils.logout_requests.LogoutRequest import LogoutRequest


class BackchannelLogoutRequest(LogoutRequest):
    def __init__(self, op_id, client_id, rp_names):
        LogoutRequest.__init__(self, op_id, client_id, rp_names, "BACKCHANNEL_LOGOUT")
        self.logout_endpoint_url = None
        self.encoded_token = None
        self.jwt_service = (
            SingletonJWTServiceProvider.get_provider().get_service_by_issuer(op_id)
        )

    def prepare_logout(self, cfg, sub, sid=None):
        """https://openid.net/specs/openid-connect-backchannel-1_0.html"""
        rp_config = (
            cfg.get("RPS", {}).get(self.client_id, {}).get("BACKCHANNEL_LOGOUT", {})
        )
        audience = rp_config.get("AUDIENCE")

        self.logout_endpoint_url = rp_config.get("LOGOUT_ENDPOINT_URL")

        token = {
            "sub": sub,
            "aud": audience,
            "jti": uuid.uuid4().hex,
            "events": {"http://schemas.openid.net/event/backchannel-logout": {}},
            "sid": sid,
        }
        self.encoded_token = self.jwt_service.get_jwt(token_args=token)

        self.iframe_src = "/proxygui/logout_iframe_callback?request_id=" + str(self.id)
        return self

    def logout(self):
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.logout_endpoint_url,
            headers=headers,
            data={"logout_token": self.encoded_token},
        )
        return response.ok

    @staticmethod
    def from_dict(data):
        new_dict = {}
        for k, v in data.items():
            if k in LogoutRequest.general_deserialization_properties:
                new_dict[k] = v
        instance = BackchannelLogoutRequest(**new_dict)
        instance.logout_endpoint_url = data["logout_endpoint_url"]
        instance.encoded_token = data["encoded_token"]
        return instance
