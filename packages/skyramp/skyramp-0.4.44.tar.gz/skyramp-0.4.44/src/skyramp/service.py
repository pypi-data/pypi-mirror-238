"""
Contains helpers for interacting with Skyramp service.
"""

class _Service:
    """
    Base class for service. This should not be used for instantiation.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=line-too-long
    def __init__(self, name, addr, alias, secure, protocol, endpoints, credentails) -> None:

        self.name = name
        self.addr = addr
        self.alias = alias
        self.secure = secure
        self.protocol = protocol
        self.endpoints = endpoints
        self.credential = credentails

    def to_json(self):
        """
        Convert the object to a dictionary
        """
        return {
            "name": self.name,
            "addr": self.addr,
            "alias": self.alias,
            "secure": self.secure,
            "protocol": self.protocol,
            "endpoints": self.endpoints,
            "credential": self.credential, 
        }
