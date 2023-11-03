# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2023, OMV"
__credits__ = ["Peter Gastinger"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Peter Gastinger"
__email__ = "peter.gastinger@omv.at"
__status__ = "Production"

# REST SDK
# https://campus.barracuda.com/product/cloudgenfirewall/api/8.3
#
# tested with 8.0.4 and 8.3.1

from enum import Enum


class RESTEndpoints(Enum):
    BOX_INFO = "/rest/control/v1/box/info"
    FF_LISTS = "/rest/config/v1/forwarding-firewall/rules/lists"
    FF_NETWORKS = "/rest/config/v1/forwarding-firewall/objects/networks"
    FF_SERVICES = "/rest/config/v1/forwarding-firewall/objects/services"
    FF_RULES = "/rest/config/v1/forwarding-firewall/rules"
    HOST_FIREWALL_RULES_BOX = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/firewall/rules?expand=true"
    FIREWALL_RULES_CLUSTER = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/servers/{server}/services/{service}/firewall/rules?expand=true"
    SERVICE_BOX = (
        "/rest/cc/v1/ranges/{range}/clusters/{cluster}/boxes/{box}/service-container"
    )
    FIREWALL_RULES_BOX = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/service-container/{service}/firewall/rules?expand=true"
    CC_RANGES = "/rest/cc/v1/ranges?expand=true"
    CC_CLUSTERS = "/rest/cc/v1/ranges/{range}/clusters?expand=true"
    CC_BOXES = "/rest/cc/v1/ranges/{range}/clusters/{cluster}/boxes?expand=true"
    #    CC_BOXES_MODELS = "/rest/cc/v1/ranges/{range}/clusters/{cluster}/boxModels"
    CC_BOX = "/rest/cc/v1/ranges/{range}/clusters/{cluster}/boxes/{box}"

    # cc managed network objects (shared-firewall not included)
    GLOBAL_NETWORKS = "/rest/cc/v1/config/global/firewall/objects/networks?expand=true"
    RANGE_NETWORKS = (
        "/rest/cc/v1/config/ranges/{range}/firewall/objects/networks?expand=true"
    )
    BOX_NETWORKS = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/firewall/objects/networks?expand=true"
    BOX_SERVICE_CONTAINER_NETWORKS = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/service-container/{service}/firewall/objects/networks?expand=true"
    CLUSTER_NETWORKS = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/firewall/objects/networks?expand=true"
    CLUSTER_SERVER_NETWORKS = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/servers/{server}/services/{service}/firewall/objects/networks?expand=true"
    CLUSTER_SERVICES_NETWORKS = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/services/{service}/firewall/objects/networks?expand=true"

    # cc managed services (shared-firewall stuff not included)
    GLOBAL_SERVICES = "/rest/cc/v1/config/global/firewall/objects/services?expand=true"
    RANGE_SERVICES = (
        "/rest/cc/v1/config/ranges/{range}/firewall/objects/services?expand=true"
    )
    BOX_SERVICES = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/firewall/objects/services?expand=true"
    BOX_SERVICE_CONTAINER_SERVICES = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/boxes/{box}/service-container/{service}/firewall/objects/services?expand=true"
    CLUSTER_SERVICES = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/firewall/objects/services?expand=true"
    CLUSTER_SERVER_SERVICES = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/servers/{server}/services/{service}/firewall/objects/services?expand=true"
    CLUSTER_SERVICES_SERVICES = "/rest/cc/v1/config/ranges/{range}/clusters/{cluster}/services/{service}/firewall/objects/services?expand=true"
