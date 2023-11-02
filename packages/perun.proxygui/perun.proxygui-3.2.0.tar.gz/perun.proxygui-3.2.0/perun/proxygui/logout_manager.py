import copy
from datetime import datetime

from perun.connector import Logger
from saml2 import samlp
from saml2.mdstore import MetadataStore
from saml2.s_utils import UnsupportedBinding
from saml2.server import Server

from perun.proxygui import jwt
from perun.proxygui.jwt import JWTServiceProvider
from perun.proxygui.user_manager import UserManager
from perun.utils import Utils
from perun.utils.CustomExceptions import InvalidJWTError
from perun.utils.logout_requests.BackchannelLogoutRequest import (
    BackchannelLogoutRequest,
)
from perun.utils.logout_requests.FrontchannelLogoutRequest import (
    FrontchannelLogoutRequest,
)
from perun.utils.logout_requests.GraphLogoutRequest import GraphLogoutRequest
from perun.utils.logout_requests.LogoutRequest import LogoutRequest
from perun.utils.logout_requests.SamlLogoutRequest import SamlLogoutRequest

SAML_REDIRECT_BINDING = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"


class LogoutManager:
    def __init__(self, cfg):
        self.user_manager = UserManager(cfg)
        self.logger = Logger.get_logger(__name__)
        self._cfg = cfg
        self.services_configuration = self.fetch_services_configuration()

    def session_exists(self, ss_sid, is_ss_session):
        ssp_sessions_collection = Utils.get_mongo_db_collection(
            "ssp_database", self._cfg
        )
        if is_ss_session:
            entries = ssp_sessions_collection.count_documents(
                {"type": "session", "key": ss_sid}
            )
        else:
            entries = 0

        return entries > 0

    def validate_request_and_extract_params(self, ssp_key, request):
        logout_methods = [
            self._resolve_rp_initiated_logout_request,
            self._resolve_saml_initiated_logout_request,
            self._resolve_rp_initiated_alternative_logout_request,
        ]

        valid, client_id, rp_sid, issuer, other_params = False, None, None, None, {}
        for logout_method in logout_methods:
            valid, client_id, rp_sid, issuer, other_params = logout_method(
                ssp_key=ssp_key, request=request
            )
            if valid:
                return valid, client_id, rp_sid, issuer, other_params

        return valid, client_id, rp_sid, issuer, other_params

    def _resolve_saml_initiated_logout_request(self, ssp_key, request):
        # todo - SAML SLO
        # also add redirect URL to other params
        return False, None, None, None, None

    def _resolve_rp_initiated_alternative_logout_request(self, ssp_key, request):
        INVALID_REQUEST = False, None, None, None, None
        logout_token = (
            request.args.get("logout_token")
            if request.form.get("logout_token") is None
            else request.form.get("logout_token")
        )

        client_id = (
            request.args.get("client_id")
            if request.form.get("client_id") is None
            else request.form.get("client_id")
        )

        if logout_token is None:
            return INVALID_REQUEST
        if (
            "client_id" in logout_token
            and client_id is not None
            and logout_token["client_id"] != client_id
        ):
            return INVALID_REQUEST

        try:
            decoded_logout_token = jwt.decode_jwt_without_verification(logout_token)
            issuer = decoded_logout_token.get("iss")
            if not issuer:
                return INVALID_REQUEST
            JWTServiceProvider.get_service_by_issuer(issuer).verify_jwt(logout_token)
        except InvalidJWTError:
            return INVALID_REQUEST

        events = logout_token.get("events")
        if (
            events is None
            or events
            != "https://openid.net/specs/openid-connect-rpinitiated-1_0.html%22"
        ):
            return INVALID_REQUEST

        sid = logout_token.get("sid")

        return True, client_id, sid, issuer, {}

    def _resolve_rp_initiated_logout_request(self, ssp_key, request):
        INVALID_REQUEST = False, None, None, None, None
        id_token_hint = (
            request.args.get("id_token_hint")
            if request.form.get("id_token_hint") is None
            else request.form.get("id_token_hint")
        )

        post_logout_redirect_uri = (
            request.args.get("post_logout_redirect_uri")
            if request.form.get("post_logout_redirect_uri") is None
            else request.form.get("post_logout_redirect_uri")
        )

        client_id = (
            request.args.get("client_id")
            if request.form.get("client_id") is None
            else request.form.get("client_id")
        )

        if id_token_hint is None:
            return INVALID_REQUEST

        try:
            decoded_token_hint = jwt.decode_jwt_without_verification(id_token_hint)
            issuer = decoded_token_hint.get("iss")
            if not issuer:
                return INVALID_REQUEST
            JWTServiceProvider.get_service_by_issuer(issuer).verify_jwt(id_token_hint)
        except InvalidJWTError as e:
            self.logger.debug(f"Error verifying JWT: {e}")
            return INVALID_REQUEST

        if (
            "client_id" in decoded_token_hint
            and client_id is not None
            and decoded_token_hint["client_id"] != client_id
        ):
            return INVALID_REQUEST

        if not client_id and "client_id" in decoded_token_hint:
            client_id = decoded_token_hint["client_id"]

        # rp_sid = self._convert_ssp_sid_to_rp_sid(client_id, session["session_id"])
        # fixme later - needs updated claims in satosa db
        rp_sid = decoded_token_hint.get("sid")  # remove me
        if rp_sid is None or (
            "sid" in decoded_token_hint and decoded_token_hint["sid"] != rp_sid
        ):
            return INVALID_REQUEST

        if (
            post_logout_redirect_uri is not None
            and not self._is_redirect_uri_registered(
                client_id, post_logout_redirect_uri
            )
        ):
            return INVALID_REQUEST

        params = {
            "client_id": client_id,
            "post_logout_redirect_uri": post_logout_redirect_uri,
        }
        if "state" in decoded_token_hint:
            params["state"] = decoded_token_hint["state"]

        return True, client_id, rp_sid, issuer, params

    def _convert_ssp_sid_to_rp_sid(self, client_id, ssp_sid):
        rp_sid = self._get_rp_sid_from_sspid_satosa(client_id, ssp_sid)
        if rp_sid is None:
            self._get_rp_sid_from_sspid_ssp(client_id, ssp_sid)
        return rp_sid

    def _get_rp_sid_from_sspid_satosa(self, client_id, ssp_sid):
        satosa_sessions_collection = Utils.get_mongo_db_collection(
            "satosa_database", self._cfg
        )

        entry = satosa_sessions_collection.find_one(
            {"client_id": client_id, "claims.ssp_session_id": ssp_sid},
            {"sid_encrypted": 1},
        )
        return entry.get("sid_encrypted") if entry else None

    def _get_rp_sid_from_sspid_ssp(self, client_id, ssp_sid):
        ssp_sessions_collection = Utils.get_mongo_db_collection(
            "ssp_database", self._cfg
        )
        current_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        entries = ssp_sessions_collection.find(
            {
                "$or": [
                    {
                        "$and": [
                            {"type": "session"},
                            {"key": ssp_sid},
                            {"expire": {"$gt": current_datetime}},
                        ]
                    },
                    {"$and": [{"type": "session"}, {"key": ssp_sid}, {"expire": None}]},
                ]
            },
            {"session_indexes_detail": 1, "_id": 0},
        )

        for entry in entries:
            session_details = entry.get("session_indexes_detail", {})
            for issuer, data in session_details.items():
                for sp, sid in data.items():
                    if sp == client_id:
                        return sid
        return None

    def _is_redirect_uri_registered(self, client_id, post_logout_redirect_uri):
        client_config = self.services_configuration.get("RPS").get(client_id)
        if client_config:
            allowed_redirect_uris = client_config.get("POST_LOGOUT_REDIRECT_URIS", [])
            return post_logout_redirect_uri in allowed_redirect_uris
        return False

    def fetch_services_configuration(self):
        """Prepares complete configuration required for logout system.
        The result format is following:
        RPS:
          client_id_1:
            LOGBACK_URI: logback_uri
            POST_LOGOUTREDIRECT_URIS:
              - redirect_uri_1
              - redirect_uri_2
            FRONTCHANNEL_LOGOUT:
              LOGOUT_URI: example_logout_uri.com
          "urn:federation:MicrosoftOnline":
            LOGBACK_URI: logback_uri
            POST_LOGOUT_REDIRECT_URIS:
              - redirect_uri_1
              - redirect_uri_2
            GRAPH_LOGOUT:
              op_id_1:
                TENANT_ID: tenant_id
                GRAPH_API_CLIENT_ID: graph_api_client_id
                GRAPH_API_CLIENT_SECRET: graph_api_client_secret
          client_id_3:
            LOGBACK_URI: logback_uri
            POST_LOGOUT_REDIRECT_URIS:
              - redirect_uri_1
              - redirect_uri_2
            BACKCHANNEL_LOGOUT:
              LOGOUT_ENDPOINT_URL: logout_endpoint_url
          client_id_4:
            LOGBACK_URI: logback_uri
            POST_LOGOUT_REDIRECT_URIS:
              - redirect_uri_1
              - redirect_uri_2
            SAML_LOGOUT:
              op_id_1:
                binding: binding
                location: url
                signkey: key_id
                keybase: keybase
                saml_idp_config: {dictionary of saml configuration for IdP Server}
                issuer_id: issuer_id_for_callback_endpoint
          client_id_5:
            LOGBACK_URI: logback_uri
            POST_LOGOUT_REDIRECT_URIS:
              - redirect_uri_1
              - redirect_uri_2
        """
        services_configuration = {"RPS": {}}

        if self._cfg["satosa_database"].get("clients_collection"):
            satosa_clients_collection = Utils.get_mongo_db_collection(
                "satosa_database", self._cfg, "clients_collection"
            )
            all_oidc_configs = satosa_clients_collection.find()
            for oidc_config in all_oidc_configs:
                backchannel_logout_uri = oidc_config.get("backchannel_logout_uri")
                frontchannel_logout_uri = oidc_config.get("frontchannel_logout_uri")
                post_logout_redirect_uris = oidc_config.get(
                    "post_logout_redirect_uri", []
                )
                post_logout_redirect_uris = [
                    item[0] for item in post_logout_redirect_uris if item
                ]
                initiate_login_uri = oidc_config.get("initiate_login_uri")

                client_id = oidc_config.get("client_id")
                if frontchannel_logout_uri and client_id:
                    frontchannel_params = {
                        "FRONTCHANNEL_LOGOUT": {"LOGOUT_URI": frontchannel_logout_uri}
                    }
                    services_configuration["RPS"][client_id] = frontchannel_params
                if backchannel_logout_uri and client_id:
                    backchannel_params = {
                        "BACKCHANNEL_LOGOUT": {
                            "LOGOUT_ENDPOINT_URL": backchannel_logout_uri
                        }
                    }
                    services_configuration["RPS"][client_id] = backchannel_params
                services_configuration["RPS"].setdefault(client_id, {})[
                    "POST_LOGOUT_REDIRECT_URIS"
                ] = post_logout_redirect_uris
                services_configuration["RPS"]["LOGBACK_URI"] = initiate_login_uri

        if "graph_api_cfg_path" in self._cfg:
            graph_configs = Utils.load_yaml_file(self._cfg["graph_api_cfg_path"])
            # todo - redirect uris, login uri
            if graph_configs:
                for op_id in graph_configs:
                    services_configuration["RPS"]["urn:federation:MicrosoftOnline"] = {
                        "GRAPH_LOGOUT": {op_id: graph_configs[op_id]}
                    }

        for issuer in self._cfg.get("issuers", []):
            # todo - redirect uris, login uri
            mds = MetadataStore(None, {})
            if "saml_metadata" in issuer:
                for md_object in issuer["saml_metadata"]:
                    mds.imp(md_object)
                for sp in mds.service_providers():
                    try:
                        # for now we only support redirect binding
                        bindings = mds.single_logout_service(
                            sp,
                            binding=SAML_REDIRECT_BINDING,
                            typ="spsso",
                        )
                        if len(bindings) > 0:
                            configuration = {
                                "binding": SAML_REDIRECT_BINDING,
                                "location": bindings[0],
                                "signkey": issuer["signeky"],
                                "keybase": issuer["keybase"],
                                "saml_idp_conf": issuer["saml_idp_config"],
                                "issuer_id": issuer["issuer_id"],
                            }
                            services_configuration["RPS"][sp] = {
                                "SAML_LOGOUT": {issuer: configuration}
                            }
                    except UnsupportedBinding:
                        pass  # does not have single_logout_service
        return services_configuration

    def prepare_logout_request(
        self, services_config, client_id, sub, rp_names, issuer, rp_sid=None
    ):
        rp_config = services_config.get("RPS", {}).get(client_id, None)

        if rp_config is None:
            request = LogoutRequest(issuer, client_id, rp_names)
        elif "BACKCHANNEL_LOGOUT" in rp_config:
            request = BackchannelLogoutRequest(issuer, client_id, rp_names)
        elif "FRONTCHANNEL_LOGOUT" in rp_config:
            request = FrontchannelLogoutRequest(issuer, client_id, rp_names)
        elif "GRAPH_LOGOUT" in rp_config:
            request = GraphLogoutRequest(issuer, client_id, rp_names)
        elif "SAML_LOGOUT" in rp_config:
            request = SamlLogoutRequest(issuer, client_id, rp_names)
        else:
            request = LogoutRequest(issuer, client_id, rp_names)
        request.prepare_logout(services_config, sub, rp_sid)

        return request

    def deserialize_request(self, data):
        logout_type = data.get("logout_type")
        if logout_type == "BACKCHANNEL_LOGOUT":
            return BackchannelLogoutRequest.from_dict(data)
        elif logout_type == "GRAPH_LOGOUT":
            return GraphLogoutRequest.from_dict(data)
        else:
            return LogoutRequest.from_dict(data)

    def complete_service_names(self, clients_data, rp_names):
        # todo - jazyky brát z config option languages - brát průnik,
        #  issuer bude mapa {issuer: pretty_name}
        # todo - pěkná funkce na vyčítání (fallback když je jenom japonská
        #  verze atd...)

        client_ids = {}  # client_id: [issuer1, issuer2]
        names = []
        for client_id, _, issuer in clients_data:
            if client_id not in client_ids:
                client_ids[client_id] = []
            if issuer not in client_ids[client_id]:
                client_ids[client_id].append(issuer)

        for client_id, issuers in client_ids.items():
            client_names = rp_names.get(client_id, {"en": client_id, "cs": client_id})
            if len(issuers) > 1:
                for issuer in issuers:
                    base_names = copy.deepcopy(client_names)
                    for lang in base_names:
                        base_names[lang] = f"{issuer}: {base_names[lang]}"
                    names.append(base_names)
            else:
                names.append(client_names)
        return names

    def check_saml_callback(self, request, issuer_id):
        """
        Checks, if request is a valid response to initiated SAML logout request.
        :param request: request from SP
        :param issuer_id: identifier of issuer used for callback
        :return: True if request is a valid Logout response, False otherwise
        """
        if len(self._cfg.get("issuers", [])) == 0:
            self.logger.error(
                "SAML callback endpoint: issuers are missing in the configuration!"
            )
            return False

        if not request.args.get("SAMLResponse"):
            self.logger.info(
                f"No 'SAMLresponse' in callback logout request for issuer {issuer_id}."
            )
            return False

        issuer = next(
            (iss for iss in self._cfg["issuers"] if iss["issuer_id"] == issuer_id), None
        )
        if not issuer:
            self.logger.info(
                f"Unknown issuer identifier in callback logout request: {issuer_id}."
            )
        idp = Server(issuer["config"])

        try:
            logout_response = idp.parse_logout_request_response(
                request["SAMLResponse"],
                "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            )
            return (
                logout_response.status
                and logout_response.status.status_code.value == samlp.STATUS_SUCCESS
            )

        except Exception as err:
            self.logger.debug(f"Unable to parse logout request response {err}")
        return False
