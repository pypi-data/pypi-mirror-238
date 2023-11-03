import pytest
import responses

from barracuda_api.barracuda import BarracudaSession
from barracuda_api.exceptions import BarracudaEntryAlreadyExistsException

get_lists = {"lists": ["Mechelen"]}

create_list = {"name": "test-entry"}


@responses.activate
def test_ff_lists01():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists",
        json=get_lists,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert "Mechelen" in bs.get_ff_lists()["lists"]
    assert len(responses.calls) == 1


@responses.activate
def test_ff_lists02():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists?rcsMessage=added-via-REST-api",
        json=create_list,
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        bs.create_ff_list("test-entry")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_lists03():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/test-entry?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        bs.delete_ff_list("test-entry")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_lists04():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/test-entry?rcsMessage=added-via-REST-api",
        json={},
        status=500,
    )
    with pytest.raises(Exception):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            bs.delete_ff_list("test-entry")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_lists05():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists?rcsMessage=added-via-REST-api",
        json=create_list,
        status=409,
    )
    with pytest.raises(BarracudaEntryAlreadyExistsException):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            bs.create_ff_list("test-entry")
    assert len(responses.calls) == 1
