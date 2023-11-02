from perun.utils.logout_requests.LogoutRequest import LogoutRequest
import urllib.parse


class FrontchannelLogoutRequest(LogoutRequest):
    def __init__(self, op_id, client_id, rp_names):
        LogoutRequest.__init__(self, op_id, client_id, rp_names, "FRONTCHANNEL_LOGOUT")

    def prepare_logout(self, cfg, sub, sid=None):
        """https://openid.net/specs/openid-connect-frontchannel-1_0.html"""

        rp_config = (
            cfg.get("RPS", {}).get(self.client_id, {}).get("FRONTCHANNEL_LOGOUT", {})
        )
        logout_uri = rp_config.get("LOGOUT_URI")

        if not logout_uri:
            return self

        self.iframe_src = logout_uri
        if sid is not None:
            params = {"iss": self.op_id, "sid": sid}
            self.iframe_src += "?" + urllib.parse.urlencode(params)
        return self
