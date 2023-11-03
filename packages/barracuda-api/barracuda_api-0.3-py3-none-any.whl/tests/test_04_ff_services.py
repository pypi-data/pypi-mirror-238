import pytest
import responses

from barracuda_api.barracuda import BarracudaSession
from barracuda_api.exceptions import (
    BarracudaEntryNotFoundException,
    BarracudaEntryAlreadyExistsException,
)

get_services = {
    "objects": [
        "Any",
        "FTP",
        "DNS",
        "DNS-TCP",
        "HTTP",
        "HTTPS",
        "HTTP+S",
        "Any-TCP",
        "Any-UDP",
    ]
}


@responses.activate
def test_ff_svc01():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_service("tcp-test", "tcp", ["12345"])
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc02():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services/test-123",
        json={},
        status=404,
    )
    with pytest.raises(BarracudaEntryNotFoundException):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.get_ff_objects_services_by_name("test-123")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc03():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services?rcsMessage=added-via-REST-api",
        json={},
        status=409,
    )
    with pytest.raises(BarracudaEntryAlreadyExistsException):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.create_ff_objects_service("tcp-test", "tcp", ["12345"])
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc04():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with pytest.raises(AssertionError):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.create_ff_objects_service("tcp-test", "rsvp", [])
    assert len(responses.calls) == 0


@responses.activate
def test_ff_svc05():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services",
        json=get_services,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_objects_services()
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc06():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services/TCP-123",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.delete_ff_objects_services("TCP-123")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc07():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_objects_service("udp-test", "udp", "12345")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_svc08():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/objects/services",
        json=get_services,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_objects_services(True)
    assert len(responses.calls) == 1
