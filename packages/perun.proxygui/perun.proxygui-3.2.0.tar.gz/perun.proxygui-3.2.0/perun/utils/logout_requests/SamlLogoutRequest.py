import base64
import urllib.parse
from perun.connector import Logger
from saml2.server import Server
from perun.utils.logout_requests.LogoutRequest import LogoutRequest
from flask import url_for


class SamlLogoutRequest(LogoutRequest):
    """Prepares SAML request. Currently supports only redirect binding
    (called in iframe directly), expecting callback to our endpoint."""

    # todo - check if logout for whole sub is handled correctly

    def __init__(self, op_id, client_id, rp_names):
        LogoutRequest.__init__(self, op_id, client_id, rp_names, "SAML_LOGOUT")
        self.logger = self.logger = Logger.get_logger(__name__)

    def prepare_logout(self, cfg, sub, sid=None):
        rp_config = (
            cfg.get("RPS", {})
            .get(self.client_id, {})
            .get("SAML_LOGOUT", {})
            .get(self.op_id)
        )

        if (
            rp_config.get("binding")
            == "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        ):
            saml_request = self.prepare_saml_request(
                sub, sid, rp_config, rp_config["saml_idp_conf"]
            )
            encoded_request = base64.b64encode(saml_request.encode("utf-8")).decode(
                "utf-8"
            )

            callback_url = url_for(
                "gui.logout_saml_callback",
                issuer_id=rp_config.get("issuer_id"),
                _external=True,
            )
            params = {"SAMLRequest": encoded_request, "RelayState": callback_url}
            self.iframe_src = (
                f"{rp_config['location']}?{urllib.parse.urlencode(params)}"
            )
        # todo - add separate SAML redirect endpoint, so we could support other bindings
        # iFrame --> redirect endpoint sends request to SP --> our callback endpoint

    def prepare_saml_request(self, sub, sid, rp_config, idp_config):
        idp = Server(idp_config)
        lreq_id, lreq = idp.create_logout_request(
            rp_config["location"],
            issuer_entity_id=self.op_id,
            subject_id=sub,
            name_id="",  # todo - retrieve from DB in the future, don't use sub?
            session_indexes=[sid],
            sign=True,
        )
        return lreq
