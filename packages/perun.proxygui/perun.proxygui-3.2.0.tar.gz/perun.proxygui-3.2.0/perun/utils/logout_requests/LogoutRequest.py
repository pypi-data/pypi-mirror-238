import itertools


class LogoutRequest:
    """
    Object representing a logout request to be rendered in an iframe
    for specific RP based on configuration options.
    """

    id_iter = itertools.count()
    general_deserialization_properties = ["op_id", "client_id", "rp_names"]

    def __init__(self, op_id, client_id, rp_names, logout_type="UNSUPPORTED_LOGOUT"):
        self.id = next(self.id_iter)  # for gui to know which icon to update
        self.client_id = client_id
        self.op_id = op_id  # irrelevant for some logout types
        self.rp_names = rp_names  # {"cs": <cs_name>, ...}
        self.iframe_src = None  # iFrame to be generated
        self.logout_type = logout_type

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "op_id": self.op_id,
            "rp_names": self.rp_names,
            "logout_type": self.logout_type,
            "iframe_src": self.iframe_src,
        }

    @staticmethod
    def from_dict(data):
        new_dict = {}
        for k, v in data.items():
            if k in LogoutRequest.general_deserialization_properties:
                new_dict[k] = v
        instance = LogoutRequest(**new_dict)
        return instance

    def prepare_logout(self, cfg, sub, sid=None):
        pass

    def logout(self):
        return False
