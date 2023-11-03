# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2022, OMV"
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


import requests
from urllib.parse import urljoin
from .exceptions import (
    BarracudaEntryAlreadyExistsException,
    BarracudaEntryNotFoundException,
)
from .endpoints import RESTEndpoints

requests.packages.urllib3.disable_warnings()

import http.client
import logging
import logging.handlers
from datetime import datetime
import ipaddress


class BarracudaSession(requests.Session):
    """
    A class to represent parts of the Barracuda API
    """

    def __init__(
        self,
        endpoint_ip,
        api_token,
        endpoint_port=8443,
        verify=False,
        logfile="barracuda.log",
        debug=False,
        headers={},
        proxies={},
        default_rcs_message="via REST api",
    ):
        super().__init__()
        self.api_token = api_token
        self.endpoint_ip = endpoint_ip
        self.base_url = f"https://{endpoint_ip}:{endpoint_port}"
        self.verify = verify
        self.logfile = logfile
        self.debug = debug
        self._logging()
        self.headers.update(
            {
                "Accept": "application/json",
                #    "Content-Type": "application/json",
                "X-API-Token": api_token,
            }
        )
        self.headers.update(headers)
        self.logger.debug(f"Headers: {self.headers}")
        self.proxies.update(proxies)
        self.default_rcs_message = default_rcs_message
        if not verify:
            self.trust_env = False

    def _logging(self):
        """Initialize logging"""
        self.logger = logging.getLogger("BARRACUDA")
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
            http.client.HTTPConnection.debuglevel = 1
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        mask_pattern = []
        if self.api_token:
            mask_pattern.append(self.api_token)

        if self.logfile:
            fh = logging.handlers.RotatingFileHandler(
                self.logfile, encoding="utf-8", maxBytes=100000000, backupCount=5
            )
            if self.debug:
                fh.setLevel(logging.DEBUG)
            fh.setFormatter(RedactingFormatter(formatter, patterns=mask_pattern))
            self.logger.addHandler(fh)

    def request(self, method, url, *args, **kwargs):
        if type(url) is RESTEndpoints:
            url = url.value
        if method.lower() in ["post", "delete", "patch", "put"]:
            rcsMessage = self.default_rcs_message.replace(" ", "-")
            url += f"?rcsMessage={rcsMessage}"
        url = urljoin(self.base_url, url)
        self.logger.debug(f"Send: {url} {str(kwargs)}")
        response = super().request(method, url, *args, **kwargs)
        if not response.encoding:
            response.encoding = "utf-8"
        self.logger.debug(
            f"Received: {response.text} status_code: {str(response.status_code)}"
        )
        if response.status_code in [200]:
            return response.json()
        elif response.status_code in [204]:
            return True
        else:
            try:
                code = response.json()["code"]
                message = response.json()["message"]
            except Exception as e:
                code = "err"
                message = str(e)
            if response.status_code == 409:
                raise BarracudaEntryAlreadyExistsException(
                    f"{response.status_code}: {code} - {message}"
                )
            elif response.status_code == 404:
                raise BarracudaEntryNotFoundException(
                    f"{response.status_code}: {code} - {message}"
                )
            else:
                raise Exception(f"{response.status_code}: {code} - {message}")

    def _get_firewall_url(self, args):
        """
        Return the url for firewall rules

        """
        url = RESTEndpoints.FF_RULES.value
        if (
            args.get("range", "") != ""
            and args.get("cluster", "") != ""
            and args.get("box", "") != ""
        ):
            url = RESTEndpoints.FF_RULES_BOX.value.format(
                range=args.get("range"),
                cluster=args.get("cluster"),
                box=args.get("box"),
            )
        if (
            args.get("range", "") != ""
            and args.get("cluster", "") != ""
            and args.get("service", "") != ""
            and args.get("server", "") != ""
        ):
            url = RESTEndpoints.FF_RULES_CLUSTER.value.format(
                range=args.get("range"),
                cluster=args.get("cluster"),
                service=args.get("service"),
                server=args.get("server"),
            )
        return url

    def get_box_info(self):
        """
        Return box infos
        """
        self.logger.debug("Getting box info")
        return self.get(RESTEndpoints.BOX_INFO)

    def get_ff_lists(self):
        """
        Return forwarding firewall lists
            Returns:
                lists (list): existing lists, e.g. ["list1","list2"]
        """
        self.logger.debug("Get lists")
        return self.get(RESTEndpoints.FF_LISTS)

    def create_ff_list(self, name):
        """
        Create forwarding firewall list
            Parameters:
                name (str): name of new list
            Returns:
                True or raises an exception
        """
        self.logger.debug("Create forwarding firewall list entry")
        return self.post(
            RESTEndpoints.FF_LISTS,
            json={"name": name},
        )

    def delete_ff_list(self, name):
        """
        Delete forwarding firewall list
            Parameters:
                name (str): name of new list
            Returns:
                True or raises an exception
        """
        self.logger.debug("Delete forwarding firewall list entry")
        return self.delete(f"{RESTEndpoints.FF_LISTS.value}/{name}")

    def get_ff_objects_networks(self, expand=False):
        """
        Return forwarding firewall network objects
            Parameters:
                expand (bool): return expanded results, more than just the name
            Returns:
                objects (list): existing objects, e.g. {"objects": ["o1","o2"]}
        """
        self.logger.debug("Get network objects")
        url = RESTEndpoints.FF_NETWORKS.value
        if expand:
            url += "?expand=true"
        return self.get(url)

    def get_ff_objects_networks_by_name(self, name):
        """
        Return forwarding firewall network object by name
            Parameters:
                name (str): name of network object
            Returns:
                objects (dict): existing object
        """
        self.logger.debug("Get network objects by name")
        return self.get(f"{RESTEndpoints.FF_NETWORKS.value}/{name}")

    def delete_ff_objects_network(self, name):
        """
        Delete forwarding firewall network object
            Parameters:
                name (str): name of the service
            Returns:
                True or raises an exception
        """
        self.logger.debug("Delete network object")
        return self.delete(f"{RESTEndpoints.FF_NETWORKS.value}/{name}")

    def _check_values_network(self, values, is_reference):
        # ngEnumLabel: List [ "generic", "singleIPv4Address", "listIPv4Address", "singleIPv4Network", "listIPv4Network", "hostname", "singleIPv6Address", "listIPv6Address", "singleIPv6Network", "listIPv6Network" ]
        # object_type = "singleIPv4Address"
        object_type = "generic"  # changes the icon
        value_list = []

        if type(values) is str:
            values = [values]

        for value in values:
            if is_reference:
                value_list.append({"references": value})
            else:
                assert ipaddress.ip_network(
                    value, False
                ), "Value has to be an IP address/network"
                value_list.append({"entry": {"ip": value}})

        return object_type, value_list

    def create_ff_objects_network(
        self, name, values, is_reference=False, excluded=None
    ):
        """
        Create forwarding firewall network objects
            Parameters:
                name (str): name of service object
                values (str|list): values to add to network object
                is_reference (bool): if set, then all the values are not IP addresses, but references to existing objects
                excluded (str|list): values to exclude in a network object
            Returns:
                True or raises an exception
        """
        self.logger.debug("Create network object")
        object_type, included = self._check_values_network(values, is_reference)

        new_object = {
            "name": name,
            "color": "#005D9A",  # borealis blue
            "type": object_type,
            "comment": f'{self.default_rcs_message} {datetime.now().strftime("%Y%m%dT%H%M%S")}',
            "included": included,
        }

        if excluded:
            _, excluded = self._check_values_network(excluded, is_reference)
            new_object["excluded"] = excluded

        self.logger.debug(new_object)
        return self.post(url=RESTEndpoints.FF_NETWORKS, json=new_object)

    def get_ff_objects_services(self, expand=False):
        """
        Return forwarding firewall services objects
            Parameters:
                expand (bool): return expanded results, more than just the name
            Returns:
                objects (list): existing objects, e.g. {"objects": ["any","o2"]}
        """
        self.logger.debug("Get services objects")
        url = RESTEndpoints.FF_SERVICES.value
        if expand:
            url += "?expand=true"
        return self.get(url)

    def delete_ff_objects_services(self, name):
        """
        Delete forwarding firewall services object
            Parameters:
                name (str): name of service
            Returns:
                True or raises an exception
        """
        self.logger.debug("Delete services object")
        return self.delete(f"{RESTEndpoints.FF_SERVICES.value}/{name}")

    def _check_values_services(self, protocol, ports):
        assert protocol.lower() in ["tcp", "udp"], f"Invalid protocol {protocol}"
        entries = []
        if type(ports) is str:
            ports = [ports]

        entries.append({"entry": {"protocol": protocol, protocol: {"ports": ports}}})

        return entries

    def create_ff_objects_service(self, name, protocol, ports):
        """
        Create forwarding firewall services objects
            Parameters:
                name (str): name of service object
                protocol (str): protocol, either TCP or UDP
                ports (list): ports for service, list of strings, range is also supported
            Returns:
                True or raises an exception
        """
        self.logger.debug("Create service object")

        new_object = {
            "name": name,
            "comment": f'{self.default_rcs_message} {datetime.now().strftime("%Y%m%dT%H%M%S")}',
            "color": "#005D9A",  # borealis blue
            "entries": self._check_values_services(protocol, ports),
        }
        self.logger.debug(new_object)
        return self.post(url=RESTEndpoints.FF_SERVICES, json=new_object)

    def get_ff_objects_services_by_name(self, name):
        """
        Return forwarding firewall network object by name
            Parameters:
                name (str): name of services object
            Returns:
                objects (dict): existing object
        """
        self.logger.debug("Get service objects by name")
        return self.get(f"{RESTEndpoints.FF_SERVICES.value}/{name}")

    def get_ff_rules(
        self, expand=False, list="", range="", cluster="", box="", service="", server=""
    ):
        """
        Return forwarding firewall rules
            Parameters:
                expand (bool): return expanded results, more than just the name
                list (str): rule list (optional)
                range (int): range number
                cluster (str): name of cluster (if cc is used)
                box (str): name of box  (if ff rule is defined per box in a cluster)
                service (str): name of service (if ff rule is defined on a cluster level)
                server (str): name of server (if ff rule is defined on a cluster level)
            Returns:
                rules (list): existing rules
        """
        self.logger.debug("Get rules")
        url = self._get_firewall_url(locals())
        if list:
            url += f"/lists/{list}"
        if expand:
            url += "?expand=true"
        return self.get(url)

    def delete_ff_rule(
        self, name, list="", range="", cluster="", box="", service="", server=""
    ):
        """
        Delete forwarding firewall rule
            Parameters:
                name (str): name of rule
                list (str): rule list (optional)
                range (int): range number
                cluster (str): name of cluster (if cc is used)
                box (str): name of box  (if ff rule is defined per box in a cluster)
                service (str): name of service (if ff rule is defined on a cluster level)
                server (str): name of server (if ff rule is defined on a cluster level)
            Returns:
                True or raises an exception
        """
        self.logger.debug("Delete rule object")
        url = self._get_firewall_url(locals())
        if list:
            url += f"/lists/{list}"
        return self.delete(f"{url}/{name}")

    def get_ff_rule_by_name(
        self, name, list="", range="", cluster="", box="", service="", server=""
    ):
        """
        Get forwarding firewall rule
            Parameters:
                name (str): name of rule
                list (str): rule list (optional)
                range (int): range number
                cluster (str): name of cluster (if cc is used)
                box (str): name of box  (if ff rule is defined per box in a cluster)
                service (str): name of service (if ff rule is defined on a cluster level)
                server (str): name of server (if ff rule is defined on a cluster level)
            Returns:
                True or raises an exception
        """
        self.logger.debug(f"Get rule object by name {name} in list {list}")
        url = self._get_firewall_url(locals())
        if list:
            url += f"/lists/{list}"
        return self.get(f"{url}/{name}")

    def update_ff_rule(
        self,
        name,
        list="",
        range="",
        cluster="",
        box="",
        service="",
        server="",
        content={},
    ):
        """
        Update forwarding firewall rule
            Parameters:
                name (str): name of rule
                list (str): rule list (optional)
                range (int): range number
                cluster (str): name of cluster (if cc is used)
                box (str): name of box  (if ff rule is defined per box in a cluster)
                service (str): name of service (if ff rule is defined on a cluster level)
                server (str): name of server (if ff rule is defined on a cluster level)
                content (dict): updated rule content
            Returns:
                True or raises an exception
        """
        self.logger.debug("Update rule object")
        url = self._get_firewall_url(locals())
        if list:
            url += f"/lists/{list}"
        return self.patch(f"{url}/{name}", json=content)

    def _convert_objects(self, obj, is_service=False):
        new_object = {}
        assert type(obj) is list, f"Object {obj} not of type list - {type(obj)}"

        if len(obj) == 0:
            return {"references": "Any"}
        elif len(obj) == 1:
            return {"references": obj[0]}
        else:
            if not is_service:
                new_object = {
                    "explicit": {
                        "excluded": [],
                        "included": [],
                        "name": "<explicit>",
                        "type": "generic",
                    }
                }
                for o in obj:
                    new_object["explicit"]["included"].append({"references": o})
            else:
                new_object = {
                    "explicit": {
                        "entries": [],
                        "name": "<explicit>",
                    }
                }
                for o in obj:
                    new_object["explicit"]["entries"].append({"references": o})

        return new_object

    def create_ff_rule(
        self,
        name,
        src,
        dst,
        svc,
        comment="",
        placement="bottom",
        action="pass",
        list="",
        cascaded_rule_list="",
        custom_action_object="",
        range="",
        cluster="",
        box="",
        service="",
        server="",
    ):
        """
        Create forwarding firewall services objects. We only want to use references, not direct IP addresses/ports
            Parameters:
                name (str): name of rule
                src (list): source address names
                dst (list): destination address names
                svc (list): services names
                placement (str): placement of new rule, by default at the bottom, only top and bottom are supported right now
                comment (str): optional comment
                action (str): pass, block, deny, cascade, cascadeback, custom
                list (str): optional rule list where to add the rule
                cascaded_rule_list (str): if action is cascade, we need a rule_list to which we cascade to
                custom_action_object (dict): if the default actions are not good enough, you can provide a custom action (e.g. with IPS policy)
                list (str): rule list (optional)
                range (int): range number
                cluster (str): name of cluster (if cc is used)
                box (str): name of box  (if ff rule is defined per box in a cluster)
                service (str): name of service (if ff rule is defined on a cluster level)
                server (str): name of server (if ff rule is defined on a cluster level)
            Returns:
                True or raises an exception
        """
        self.logger.debug("Create firewall rule")
        # ngEnumLabel: List [ "exact", "top", "bottom", "before", "after" ]

        assert placement.lower() in [
            "top",
            "bottom",
        ], f"Placement {placement} not possible, only top and bottom supported at the moment"

        if action == "pass":
            action_object = {
                "connection": {
                    "explicit": {
                        "failover": {"policy": "none"},
                        "ipVersion": "IPv4",
                        "timeout": 30,
                        "nat": {
                            "translatedSourceIp": "originalSourceIp",
                            "weight": 1,
                        },
                    }
                },
                "type": action,
            }
        elif action in ["cascade", "cascadeback", "block", "deny"]:
            action_object = {"type": action}
            if action == "cascade":
                assert len(cascaded_rule_list) > 0, "Cascaded ruleset must be defined"
                action_object = {"type": action, "ruleList": cascaded_rule_list}
        elif action == "custom":
            assert custom_action_object, "A custom action has to be defined"
            action_object = custom_action_object
        else:
            raise AssertionError(f"Action {action} invalid or not implemented yet")

        if not comment:
            comment = (
                f'{self.default_rcs_message} {datetime.now().strftime("%Y%m%dT%H%M%S")}'
            )

        new_rule = {
            "action": action_object,
            "bidirectional": False,
            "deactivated": False,
            "destination": self._convert_objects(dst),
            "dynamic": False,
            "ipVersion": "IPv4",
            "name": name,
            "service": self._convert_objects(svc, is_service=True),
            "source": self._convert_objects(src),
            "position": {"placement": placement},
            "comment": comment,
        }

        self.logger.debug(new_rule)
        url = self._get_firewall_url(
            range="", cluster="", box="", service="", server=""
        )
        if list:
            url += f"/lists/{list}"
        return self.post(url, json=new_rule)


class RedactingFormatter(object):
    def __init__(self, orig_formatter, patterns):
        self.orig_formatter = orig_formatter
        self._patterns = patterns

    def format(self, record):
        msg = self.orig_formatter.format(record)
        for pattern in self._patterns:
            msg = msg.replace(pattern, "***")
        return msg
