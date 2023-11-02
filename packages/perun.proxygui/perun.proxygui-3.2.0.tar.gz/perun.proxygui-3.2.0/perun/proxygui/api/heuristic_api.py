from satosacontrib.perun.utils.AuthEventLoggingDbModels import (
    AuthEventLoggingTable,
    UserAgentTable,
    RequestedAcrsTable,
    LoggingSpTable,
    UpstreamAcrsTable,
)
from sqlalchemy import create_engine, MetaData, select
from user_agents import parse
from socket import getnameinfo
import json


# Queries for fetching data from AuthEventMicroService
class AuthEventLoggingQueries:
    def __init__(self, cfg):
        # Vars for storing arrays with DB responses
        self.auth_result = None  # Auth data, Upstream, Requested and Services
        self.user_agents = None  # User agents and upstream logs
        self.time_result = None  # Many AuthEvent logs
        # Nunbers of retrieved rows from DB for various data
        self.few_time_logs = cfg["heuristic_page"]["few_time_logs"]
        self.some_time_logs = cfg["heuristic_page"]["some_time_logs"]
        self.many_time_logs = cfg["heuristic_page"]["many_time_logs"]
        # DB connect string
        self.logging_db = cfg["auth_event_logging"]["logging_db"]
        # REFEDS profile for MFA.
        self.REFEDS_MFA = "https://refeds.org/profile/mfa"
        # Microsoft authentication context for MFA.
        self.MS_MFA = "http://schemas.microsoft.com/claims/multipleauthn"
        # Contexts trusted as multifactor authentication, in the order of
        # preference (for replies).
        self.MFA_CONTEXTS = [self.REFEDS_MFA, self.MS_MFA]
        # Answers to be displayed in UI
        self.REQUEST_MFA_VALUE = {
            "required": "MFA required",
            "preferred": "MFA preferred",
            "other": "Other auth.",
        }

    # Modify ACRs value from string to list
    # '["acr1","acr2"]' -> ['acr1', 'acr2']
    # "acr1" -> ['acr1']
    def strip_acrs(self, acr):
        listed_acrs = acr.strip("][").split(",")
        for i, item in enumerate(listed_acrs):
            listed_acrs[i] = item.strip(" ").strip('"')
        return listed_acrs

    # Simple function for return type of requested authenticaton
    def requested_acr_status(self, raw_acr):
        acr = self.strip_acrs(raw_acr)
        if not acr:
            return self.REQUEST_MFA_VALUE["other"]
        elif len(set(acr) - set(self.MFA_CONTEXTS)) == 0:
            return self.REQUEST_MFA_VALUE["required"]
        elif acr[0] in self.MFA_CONTEXTS:
            return self.REQUEST_MFA_VALUE["preferred"]
        else:
            return self.REQUEST_MFA_VALUE["other"]

    # Beasic checker if MFA was performad based on upstream_acrs value
    def upstream_acr_status(self, acr):
        mfa_status = next((mfa for mfa in self.MFA_CONTEXTS if mfa in acr), None)
        return mfa_status is not None

    # Return specific number of logs from main table
    # Also joined in some requests
    def get_auth_logs(self, user):
        engine = create_engine(self.logging_db)
        with engine.connect() as cnxn:
            meta_data = MetaData(bind=engine)
            MetaData.reflect(meta_data)

            auth_table = AuthEventLoggingTable().__table__
            agents_table = UserAgentTable().__table___
            upstream_table = UpstreamAcrsTable().__table__
            requested_table = RequestedAcrsTable().__table__
            services_table = LoggingSpTable().__table__

            # Returns last 'self.short_time_logs' logs
            # for specific user, sorted
            # by decending time joined with upstream ACRs, requested ACRs
            # and services table
            query = (
                select(
                    auth_table.c.day.label("day"),
                    auth_table.c.geolocation_city.label("geolocation_city"),
                    auth_table.c.geolocation_country.label("geolocation_country"),
                    auth_table.c.ip_address.label("ip_address"),
                    requested_table.c.value.label("requested_value"),
                    upstream_table.c.value.label("upstream_value"),
                    services_table.c.name.label("name"),
                    services_table.c.identifier.label("identifier"),
                )
                .select_from(auth_table)
                .join(
                    requested_table,
                    requested_table.c.id == auth_table.c.requested_acrs_id,
                )
                .join(
                    upstream_table, upstream_table.c.id == auth_table.c.upstream_acrs_id
                )
                .join(services_table, services_table.c.id == auth_table.c.sp_id)
                .where(auth_table.c.user == user)
                .order_by(auth_table.c.day.desc())
                .limit(self.few_time_logs)
            )
            response = cnxn.execute(query).fetchall()
            self.auth_result = [r._asdict() for r in response]

            # Return last 'self.long_time_logs' logs
            # for user, sorted by time for logging graph
            query = (
                auth_table.select()
                .order_by(auth_table.c.day.desc())
                .where(auth_table.c.user == user)
                .limit(self.many_time_logs)
            )
            response = cnxn.execute(query).fetchall()
            self.time_result = [r._asdict() for r in response]

            # Returns joined values from user_agents and upstream_acrs
            # joined on auth_event_logging table
            query = (
                select(
                    agents_table.c.value.label("agent_value"),
                    upstream_table.c.value.label("upstream_value"),
                )
                .select_from(auth_table)
                .join(agents_table, agents_table.c.id == auth_table.c.user_agent_id)
                .join(
                    upstream_table, upstream_table.c.id == auth_table.c.upstream_acrs_id
                )
                .where(auth_table.c.user == user)
                .order_by(auth_table.c.day.desc())
                .limit(self.some_time_logs)
            )
            response = cnxn.execute(query).fetchall()
            # Returned dictionary:
            # {"agents_value": "val", "upstream_value": "val"}
            self.user_agents = [r._asdict() for r in response]

    # ----------------- Retrieving methods --------------
    # Get information about last n cities (city name, timestamp, MFA performaed status)
    def get_last_n_cities(self):
        if self.auth_result is None:
            return []

        cities = []

        # Retrieve relevant data from resluts
        for item in self.auth_result:
            city = item["geolocation_city"]
            country = item["geolocation_country"]
            time = item["day"].strftime("%d. %m. %Y %H:%M")
            value = city + ", " + country + " (" + time + ")"

            cities.append(
                {
                    "value": value,
                    "mfa": self.upstream_acr_status(item["upstream_value"]),
                }
            )

        return cities

    # Retrieve inormation about last n IP addresses connected from
    # (IP address, hostname lookup, MFA performed)
    def get_last_n_ips(self):
        if self.auth_result is None:
            return []

        ips = []
        for item in self.auth_result:
            ip = item["ip_address"]
            ip_lookup = getnameinfo((ip, 0), 0)[0]
            ip_string = ip if (ip == ip_lookup) else ip + " (" + ip_lookup + ")"
            city = item["geolocation_city"]
            country = item["geolocation_country"]
            value = ip_string + ", " + city + ", " + country

            ips.append(
                {
                    "value": value,
                    "mfa": self.upstream_acr_status(item["upstream_value"]),
                }
            )

        return ips

    # Retrive time statisctic from last n logs in AuthLogging table
    # retrun list in format to show Javascript graph [{"label": "8:00","value": 4},...]
    def get_last_n_times(self):
        if self.time_result is None:
            return []

        # Prefill labels - showing even empty colums
        times = [
            {
                "label": str(i) + ":00",
                "value": sum(1 for item in self.time_result if item["day"].hour == i),
            }
            for i in range(1, 25)
        ]
        return json.dumps(times)

    # Retieve data of used user agnets - compress same user agent and sort them by
    # usage, MFA perfomed is True if it was performed at least once on that
    # specific user agent
    def get_unique_user_agents(self):
        if self.user_agents is None:
            return []

        agents = []

        for item in self.user_agents:
            # Create default dictionary
            mfa_performed = self.upstream_acr_status(item["upstream_value"])
            parsed_agent = str(parse(item["agent_value"]))

            index = next(
                (i for i, item in enumerate(agents) if item["label"] == parsed_agent),
                None,
            )
            if index is None:  # NEW User agent
                agents.append(
                    {
                        "label": parsed_agent,
                        "value": 1,
                        "mfa": mfa_performed,
                    }
                )
            else:  # Alredy existing user agent, only actualize data
                agents[index]["value"] += 1
                agents[index]["mfa"] |= mfa_performed

        return sorted(agents, key=lambda d: d["value"], reverse=True)

    # Retrieve data of used services, their name and identifier
    # Also with type of requested ACRs and upstream ACRs
    def get_last_n_services(self):
        if self.auth_result is None:
            return []

        services = []

        for item in self.auth_result:
            requested_acrs = self.requested_acr_status(item["requested_value"])
            upstream_acrs = self.upstream_acr_status(item["upstream_value"])
            services.append(
                {
                    "name": item["name"],
                    "identifier": item["identifier"],
                    "requested_acrs": requested_acrs,
                    "upstream_acrs": upstream_acrs,
                }
            )
        return services
