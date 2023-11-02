import requests
from perun.connector import Logger

from perun.utils.logout_requests.LogoutRequest import LogoutRequest


class GraphLogoutRequest(LogoutRequest):
    auth_endpoint = "https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token"
    logout_endpoint = (
        "https://graph.microsoft.com/v1.0/users/"
        "{userPrincipalName}/revokeSignInSessions"
    )

    def __init__(self, op_id, client_id, rp_names):
        LogoutRequest.__init__(self, op_id, client_id, rp_names, "GRAPH_LOGOUT")
        # parameters stored in server-side session
        self.access_token = None
        self.user_principal_name = None
        self.logger = self.logger = Logger.get_logger(__name__)

    def prepare_logout(self, cfg, sub, sid=None):
        """https://learn.microsoft.com/en-us/graph/api/user-revokesigninsessions"""

        if sid is None:
            return  # unsupported to log out only from session

        rp_config = (
            cfg.get("RPS", {})
            .get(self.client_id, {})
            .get("GRAPH_LOGOUT", {})
            .get(self.op_id, {})
        )
        tenant_id = rp_config.get("TENANT_ID")
        graph_client_id = rp_config.get("GRAPH_API_CLIENT_ID")
        graph_client_secret = rp_config.get("GRAPH_API_CLIENT_SECRET")

        if not tenant_id:
            self.logger.error(
                f"TENANT_ID is missing in GRAPH_LOGOUT config "
                f"for client {self.client_id}"
            )
            return

        if not graph_client_id:
            self.logger.error(
                f"GRAPH_API_CLIENT_ID is missing in GRAPH_LOGOUT config "
                f"for client {self.client_id}"
            )
            return

        if not graph_client_secret:
            self.logger.error(
                f"GRAPH_API_CLIENT_SECRET is missing in GRAPH_LOGOUT config "
                f"for client {self.client_id}"
            )
            return

        self.access_token = self._request_access_token(
            graph_client_id, graph_client_secret, tenant_id
        )

        if self.access_token is not None:
            self.user_principal_name = sub

        self.iframe_src = "/proxygui/logout_iframe_callback?request_id=" + str(self.id)

    def logout(self):
        endpoint = GraphLogoutRequest.logout_endpoint.replace(
            "{userPrincipalName}", self.user_principal_name
        )
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
        }
        response = requests.post(url=endpoint, headers=headers)
        return response.ok

    def _request_access_token(self, graph_client_id, graph_client_secret, tenant_id):
        auth_endpoint = GraphLogoutRequest.auth_endpoint.replace(
            "{tenantId}", tenant_id
        )

        post_data = {
            "client_id": graph_client_id,
            "client_secret": graph_client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }

        response = requests.post(auth_endpoint, post_data)
        if response.ok:
            response_data = response.json()
            return response_data["access_token"]

        return None

    def to_dict(self):
        new_dict = super().to_dict()
        new_dict["access_token"] = self.access_token
        new_dict["user_principal_name"] = self.user_principal_name
        return new_dict

    @staticmethod
    def from_dict(data):
        new_dict = {}
        for k, v in data.items():
            if k in LogoutRequest.general_deserialization_properties:
                new_dict[k] = v
        instance = GraphLogoutRequest(**new_dict)
        instance.access_token = data["access_token"]
        instance.user_principal_name = data["user_principal_name"]
        return instance
