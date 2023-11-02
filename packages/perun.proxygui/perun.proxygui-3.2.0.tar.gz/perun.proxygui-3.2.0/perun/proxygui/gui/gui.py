import copy
from urllib import parse
from uuid import uuid4

import flask
import yaml
from flask import (
    Blueprint,
    request,
    url_for,
    render_template,
    make_response,
    jsonify,
    session,
    redirect,
)
from flask_babel import get_locale, gettext
from flask_pyoidc.user_session import UserSession
from perun.connector.utils import Logger

from perun.proxygui.jwt import SingletonJWTServiceProvider
from perun.proxygui.logout_manager import LogoutManager
from perun.proxygui.user_manager import UserManager
from perun.utils.CustomExceptions import InvalidJWTError
from perun.proxygui.api.heuristic_api import AuthEventLoggingQueries
from perun.utils.consent_framework.consent_manager import ConsentManager

logger = Logger.Logger.get_logger(__name__)


def ignore_claims(ignored_claims, claims):
    result = dict()

    for claim in claims:
        if claim not in ignored_claims:
            result[claim] = claims[claim]

    return result


def construct_gui_blueprint(cfg, auth):
    gui = Blueprint("gui", __name__, template_folder="templates")
    consent_db_manager = ConsentManager(cfg)
    user_manager = UserManager(cfg)
    jwt_service = SingletonJWTServiceProvider.get_provider().get_service()
    logout_manager = LogoutManager(cfg)
    auth_event = AuthEventLoggingQueries(cfg)

    REDIRECT_URL = cfg["redirect_url"]
    COLOR = cfg["bootstrap_color"]
    OIDC_CFG = cfg["oidc_provider"]

    @gui.route("/authorization/<token>")
    def authorization(token):
        try:
            message = jwt_service.verify_jwt(token)
        except InvalidJWTError as e:
            return make_response(
                jsonify({gettext("fail"): f"JWT validation failed with error: '{e}'"}),
                400,
            )
        email = message.get("email")
        service = message.get("service")
        registration_url = message.get("registration_url")
        if not email or not service:
            return make_response(
                jsonify({gettext("fail"): gettext("Missing request parameter")}),
                400,
            )
        return render_template(
            "authorization.html",
            email=email,
            service=service,
            registration_url=registration_url,
            bootstrap_color=COLOR,
        )

    @gui.route("/SPAuthorization/<token>")
    def sp_authorization(token):
        try:
            message = jwt_service.verify_jwt(token)
        except InvalidJWTError as e:
            return make_response(
                jsonify({gettext("fail"): f"JWT validation failed with error: '{e}'"}),
                400,
            )
        email = message.get("email")
        service = message.get("service")
        registration_url = message.get("registration_url")
        return render_template(
            "SPAuthorization.html",
            email=email,
            service=service,
            registration_url=registration_url,
            bootstrap_color=COLOR,
        )

    @gui.route("/logout", methods=["POST", "GET"])
    def logout():
        ssp_session_id = request.cookies.get("SimpleSAMLSessionID")
        logger.debug(f"Logout call for SimpleSAMLSessionID: {ssp_session_id}")
        # todo - dbs will contain user_id and won't need to be converted in the future
        sub = user_manager.get_user_id_by_ssp_session_id(ssp_session_id)

        if ssp_session_id is None or sub is None:
            return render_template("MissingAuth.html")

        (
            valid_request,
            client_id,
            rp_sid,
            issuer,
            logout_params,
        ) = logout_manager.validate_request_and_extract_params(ssp_session_id, request)

        if valid_request:
            user_manager.logout_from_service_op(sub, ssp_session_id, client_id)

        device_active_clients = user_manager.get_active_client_ids_for_user(sub)
        session_active_clients = user_manager.get_active_client_ids_for_session(
            request.cookies.get("SimpleSAMLSessionID")
        )

        rp_names = user_manager.get_all_rp_names()
        logged_out_service = (
            {
                "from_devices": rp_sid is None,
                # user might have been logged out for all devices
                "labels": rp_names.get(client_id, client_id),
                "client_id": client_id,
            }
            if client_id is not None
            else {}
        )

        session_services = logout_manager.complete_service_names(
            session_active_clients, rp_names
        )
        device_services = logout_manager.complete_service_names(
            device_active_clients, rp_names
        )
        session["logout_params"] = logout_params if logout_params else {}
        session["init_logged_out_service"] = logged_out_service
        session["init_issuer"] = issuer  # todo - we probably don't need to save it

        resp = make_response(
            render_template(
                "Logout.html",
                logged_out_service=logged_out_service,
                session_services=session_services,
                device_services=device_services,
                default_postlogout_uri=cfg.get("default_postlogout_uri"),
                bootstrap_color=COLOR,
            )
        )
        return resp

    @gui.route("/logout_state", methods=["GET"])
    def logout_state():
        if session.get("logout_params") is None:
            # at least empty dict should be set, or logout endpoint was not visited
            return redirect(url_for("gui.logout", _external=True))

        ssp_session_id = request.cookies.get("SimpleSAMLSessionID")
        # todo - dbs will contain user_id and won't need to be converted in the future
        sub = user_manager.get_user_id_by_ssp_session_id(ssp_session_id)

        if ssp_session_id is None or sub is None:
            return render_template("MissingAuth.html")

        include_all_devices = request.args.get("from_devices", False)
        include_all_devices = include_all_devices in ["True", True, "true"]

        if include_all_devices:
            active_clients = user_manager.get_active_client_ids_for_user(sub)
            unique_client_issuer_clients = []
            for client_id, sid, issuer in active_clients:
                found = next(
                    filter(
                        lambda x: x[0] == client_id and x[2] == issuer,
                        unique_client_issuer_clients,
                    ),
                    None,
                )
                unique_client_issuer_clients.append(
                    (client_id, sid, issuer)
                ) if not found else None
                active_clients = unique_client_issuer_clients
        else:
            active_clients = user_manager.get_active_client_ids_for_session(
                ssp_session_id
            )

        rp_names = user_manager.get_all_rp_names()
        # todo - jazyky brát z config option languages - brát průnik,
        #  issuer bude mapa {issuer: pretty_name}
        # todo - pěkná funkce na vyčítání (fallback když je jenom japonská verze atd...)
        service_configs = logout_manager.services_configuration
        logout_requests = [
            logout_manager.prepare_logout_request(
                service_configs,
                client_id,
                sub,
                rp_names.get(client_id, {"en": client_id, "cs": client_id}),
                issuer,
                rp_sid if include_all_devices else None,
            ).to_dict()
            for (client_id, rp_sid, issuer) in active_clients
        ]

        session["logout_requests"] = logout_requests
        init_logged_out_client_id = session["init_logged_out_service"].get("client_id")
        session["init_logged_out_service"]["logback_url"] = (
            service_configs.get("RPS", {})
            .get(init_logged_out_client_id, {})
            .get("logback_url")
        )

        main_issuer = cfg.get("issuers", [{}])[0].get("issuer")
        if not main_issuer:
            logger.error("Main issuer not set!")
            return make_response(
                jsonify({gettext("fail"): "Invalid endpoint configuration."}),
                400,
            )
        user_id = user_manager.sub_to_user_id(sub, main_issuer)
        if not user_id:
            return render_template("MissingAuth.html")
        user_manager.logout(
            user_id=user_id,
            session_id=ssp_session_id if include_all_devices else None,
            include_refresh_tokens=include_all_devices,
        )

        resp = make_response(
            render_template(
                "logout-state.html",
                session_services=logout_requests if not include_all_devices else [],
                device_services=logout_requests if include_all_devices else [],
                bootstrap_color=COLOR,
            )
        )
        resp.delete_cookie("SimpleSAMLSessionID")
        return resp

    @gui.route("/post_logout")
    def post_logout():
        logout_params = session.get("logout_params")
        init_logged_out_service = session.get("init_logged_out_service")
        session.clear()

        if (
            logout_params is None or init_logged_out_service is None
        ):  # can be {} but not None (wrong flow then)
            return render_template("MissingAuth.html")

        if "post_logout_redirect_uri" in logout_params:
            url = logout_params["post_logout_redirect_uri"]
            if "state" in logout_params:
                state = parse.quote(logout_params["state"])
                url = f"{url}?{state}" if "?" not in url else f"{url}&{state}"
            return redirect(url)

        return render_template(
            "Post-logout.html",
            init_logged_out_service=init_logged_out_service,
            bootstrap_color=COLOR,
        )

    @gui.route("/logout_iframe_callback", methods=["GET"])
    def logout_iframe_callback():
        request_id = request.args.get("request_id")
        logout_requests = session["logout_requests"]

        current_request = next(
            (r for r in logout_requests if str(r["id"]) == request_id), None
        )

        if current_request is None:
            response = False
        else:
            req = logout_manager.deserialize_request(current_request)
            response = req.logout()
        return render_template(
            "logout-iframe.html",
            result="success" if response else response,
        )

    @gui.route("/logout_saml_callback/<issuer_id>", methods=["GET"])
    def logout_saml_callback(issuer_id):
        request_ok = logout_manager.check_saml_callback(request, issuer_id)

        return render_template(
            "logout-iframe.html",
            result="success" if request_ok else "request invalid",
        )

    @gui.route("/IsTestingSP")
    def is_testing_sp():
        return render_template(
            "IsTestingSP.html",
            redirect_url=REDIRECT_URL,
            bootstrap_color=COLOR,
        )

    @gui.route("/consent/<token>")
    def consent(token):
        try:
            ticket = jwt_service.verify_jwt(token)
        except InvalidJWTError as e:
            return make_response(
                jsonify({gettext("fail"): f"JWT validation failed with error: '{e}'"}),
                400,
            )
        data = consent_db_manager.fetch_consent_request(ticket)
        if not ticket:
            return make_response(
                jsonify({gettext("fail"): gettext("received invalid ticket")}),
                400,
            )

        months_valid = cfg["consent"]["months_valid"]
        session["id"] = data["id"]
        session["state"] = uuid4().urn
        session["redirect_endpoint"] = data["redirect_endpoint"]
        session["attr"] = ignore_claims(cfg["consent"]["ignored_claims"], data["attr"])
        session["user_id"] = data["user_id"]
        session["locked_attrs"] = data.get("locked_attrs")
        session["requester_name"] = data["requester_name"]
        session["month"] = months_valid

        warning = cfg["consent"].get("warning", None)
        with open(
            cfg["consent"]["attribute_config_path"],
            "r",
            encoding="utf8",
        ) as ymlfile:
            attr_config = yaml.safe_load(ymlfile)

        return render_template(
            "ConsentRegistration.html",
            bootstrap_color=COLOR,
            cfg=cfg,
            attr_config=attr_config,
            released_claims=copy.deepcopy(session["attr"]),
            locked_claims=session["locked_attrs"],
            requester_name=session["requester_name"],
            months=months_valid,
            data_protection_redirect=data["data_protection_redirect"],
            warning=warning,
        )

    @gui.route("/mfa-reset-verify/<token>")
    @auth.oidc_auth(OIDC_CFG["provider_name"])
    def mfa_reset_verify(token):
        try:
            reset_request = jwt_service.verify_jwt(token)
        except InvalidJWTError:
            return render_template(
                "MfaResetVerifyConfirmationFail.html",
            )
        requester_email = reset_request.get("requester_email")
        user_manager.forward_mfa_reset_request(requester_email)
        return render_template(
            "MfaResetVerifyConfirmationSuccess.html",
        )

    @gui.route("/send-mfa-reset-emails")
    @auth.oidc_auth(OIDC_CFG["provider_name"])
    def send_mfa_reset_emails():
        user_session = UserSession(flask.session, OIDC_CFG["provider_name"])
        sub = user_session.userinfo.get("sub")
        issuer = OIDC_CFG["issuer"]
        user_id = user_manager.sub_to_user_id(sub, issuer)
        locale = get_locale().language
        preferred_email = user_manager.handle_mfa_reset(
            user_id, locale, url_for("gui.mfa_reset_verify")
        )
        return render_template(
            "MfaResetEmailSent.html",
            email=preferred_email,
        )

    @gui.route("/mfa-reset")
    @auth.oidc_auth(OIDC_CFG["provider_name"])
    def mfa_reset():
        return render_template(
            "MfaResetInitiated.html",
            redirect_url=REDIRECT_URL,
            bootstrap_color=COLOR,
            referrer=request.referrer or "/",
            send_mfa_reset_emails=url_for("gui.send_mfa_reset_emails"),
        )

    @auth.oidc_auth(OIDC_CFG["provider_name"])
    @gui.route("/HeuristicGetID")
    def heuristic_get_id():
        return render_template(
            "HeuristicData.html",
            redirect_url=REDIRECT_URL,
            bootstrap_color=COLOR,
            selected=False,
        )

    @auth.oidc_auth(OIDC_CFG["provider_name"])
    @gui.route("/GetHeuristic", methods=["GET"])
    def get_heuristic():
        user_id = request.args.get("user")
        name = (
            user_manager.get_user_name(user_id)
            if cfg["perun_user_name_attribute"]
            else ""
        )
        auth_event.get_auth_logs(user_id)

        return render_template(
            "HeuristicData.html",
            redirect_url=REDIRECT_URL,
            bootstrap_color=COLOR,
            selected=True,
            user=user_id,
            name=name,
            last_n_times=auth_event.get_last_n_times(),
            user_agents=auth_event.get_unique_user_agents(),
            last_n_cities=auth_event.get_last_n_cities(),
            sps=auth_event.get_last_n_services(),
            ips=auth_event.get_last_n_ips(),
        )

    return gui
