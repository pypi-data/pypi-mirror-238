import pytest
import responses

from barracuda_api.barracuda import BarracudaSession
from barracuda_api.exceptions import BarracudaEntryNotFoundException


get_networks = {
    "objects": [
        "Any",
        "Internet",
        "Private 10",
        "Private 172",
        "Private 192",
        "RootDNS",
        "Authentication Servers",
        "Auth-MSNT",
        "Auth-RADIUS",
    ]
}

get_networks_details = {
    "objects": [
        {
            "comment": "All IPv4 addresses",
            "dynamic": False,
            "excluded": [],
            "included": [{"entry": {"ip": "0.0.0.0/0"}}],
            "name": "Any",
            "shared": False,
            "type": "generic",
        },
        {
            "comment": "All routed IPv4 addresses",
            "dynamic": False,
            "excluded": [
                {"entry": {"ip": "10.0.0.0/8"}},
                {"entry": {"ip": "172.16.0.0/12"}},
                {"entry": {"ip": "192.168.0.0/16"}},
            ],
            "included": [{"references": "Any"}],
            "name": "Internet",
            "shared": False,
            "type": "generic",
        },
        {
            "comment": "Private class A network",
            "dynamic": False,
            "excluded": [],
            "included": [{"entry": {"ip": "10.0.0.0/8"}}],
            "name": "Private 10",
            "shared": False,
            "type": "generic",
        },
        {
            "comment": "16 private class B networks",
            "dynamic": False,
            "excluded": [],
            "included": [{"entry": {"ip": "172.16.0.0/12"}}],
            "name": "Private 172",
            "shared": False,
            "type": "generic",
        },
        {
            "comment": "Private class B network",
            "dynamic": False,
            "excluded": [],
            "included": [{"entry": {"ip": "192.168.0.0/16"}}],
            "name": "Private 192",
            "shared": False,
            "type": "generic",
        },
    ]
}


@responses.activate
def test_ff_nw01():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_network(
            "int_ip_3", ["host_10.111.20.38", "host_10.111.20.39"], True
        )
    assert len(responses.calls) == 1


@responses.activate
def test_ff_nw02():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks?rcsMessage=added-via-REST-api",
        json={},
        status=400,
    )
    with pytest.raises(ValueError):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.create_ff_objects_network(
                "int_ip_3", ["host_10.111.20.38", "host_10.111.20.39"]
            )
    assert len(responses.calls) == 0


@responses.activate
def test_ff_nw03():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks/test-network?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.delete_ff_objects_network("test-network")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_nw04():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks/test-123",
        json={},
        status=404,
    )
    with pytest.raises(BarracudaEntryNotFoundException):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.get_ff_objects_networks_by_name("test-123")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_nw05():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_network("int_ip_3", "host_10.111.20.38", True)
        assert bs.create_ff_objects_network("int_ip_3", "1.2.3.4/32")
    assert len(responses.calls) == 2


@responses.activate
def test_ff_nw06():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks",
        json=get_networks,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_objects_networks()
    assert len(responses.calls) == 1


@responses.activate
def test_ff_nw07():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks",
        json=get_networks,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_objects_networks(True)
    assert len(responses.calls) == 1


@responses.activate
def test_ff_nw08():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_network(
            "int_ip_3", "host_10.111.20.38", True, "host_1.2.3.4"
        )
        assert bs.create_ff_objects_network(
            "int_ip_3", "host_10.111.20.38", True, ["host_1.2.3.4", "net_10.1.1.0--24"]
        )
    assert len(responses.calls) == 2


@responses.activate
def test_ff_nw09():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/networks?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_network("int_ip_3", "1.2.3.4")
    assert len(responses.calls) == 1
