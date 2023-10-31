# -*- coding: utf-8 -*-
"""
    pip_services4_http.build.DefaultRpcFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    DefaultRpcFactory implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from ..controller import HttpEndpoint, StatusRestController, HeartbeatRestController


class DefaultRpcFactory(Factory):
    """
    Creates RPC components by their descriptors.
    """

    HttpEndpointDescriptor = Descriptor("pip-controller", "endpoint", "http", "*", "1.0")
    StatusServiceDescriptor = Descriptor("pip-controller", "status-controller", "http", "*", "1.0")
    HeartbeatServiceDescriptor = Descriptor("pip-controller", "heartbeat-controller", "http", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultRpcFactory, self).__init__()
        self.register_as_type(self.HttpEndpointDescriptor, HttpEndpoint)
        self.register_as_type(self.StatusServiceDescriptor, StatusRestController)
        self.register_as_type(self.HeartbeatServiceDescriptor, HeartbeatRestController)
