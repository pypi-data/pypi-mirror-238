import pytest
import responses

from barracuda_api.barracuda import BarracudaSession
from barracuda_api.exceptions import (
    BarracudaEntryNotFoundException,
    BarracudaEntryAlreadyExistsException,
)

get_rule_by_name_result = {
    "action": {"connection": {"references": "Original Source IP"}, "type": "pass"},
    "bidirectional": False,
    "comment": "Allows limited LAN access from managed boxes to authentication "
    "servers, e.g., for authentication database access",
    "deactivated": False,
    "destination": {"references": "Authentication Servers"},
    "dynamic": False,
    "ipVersion": "IPv4",
    "name": "BOXES-2-LAN-AUTHENTICATION",
    "policies": {"ips": "No Scan"},
    "service": {"references": "NGF-MGMT-AUTH"},
    "source": {"references": "Any"},
}


@responses.activate
def test_ff_rule01():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/BOXES-2-LAN-AUTHENTICATION",
        json=get_rule_by_name_result,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_rule_by_name("BOXES-2-LAN-AUTHENTICATION")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule02():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/BOXES-3-LAN-AUTHENTICATION",
        json={},
        status=404,
    )
    with pytest.raises(BarracudaEntryNotFoundException):

        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.get_ff_rule_by_name("BOXES-3-LAN-AUTHENTICATION")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule03():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/FROM-proxy-TO-trust/permitall",
        json=get_rule_by_name_result,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_rule_by_name("permitall", "FROM-proxy-TO-trust")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule04():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/FROM-proxy-TO-trust/permitall2",
        json={},
        status=404,
    )
    with pytest.raises(BarracudaEntryNotFoundException):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.get_ff_rule_by_name("permitall2", "FROM-proxy-TO-trust")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule05():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules",
        json=get_rule_by_name_result,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_rules()
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule06():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/mylist?expand=true",
        json=get_rule_by_name_result,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.get_ff_rules(True, "mylist")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule07():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_rule(
            "My-rule-1",
            ["src-1", "src-2"],
            ["dst-1"],
            ["HTTP", "DNS"],
            comment="testcomment",
        )
        assert bs.create_ff_rule(
            "My-rule-2", ["src-2"], ["dst-1"], [], action="deny", placement="top"
        )
        with pytest.raises(AssertionError):
            assert bs.create_ff_rule(
                "My-rule-3", ["src-2"], [], [], action="cascade", placement="top"
            )
        assert bs.create_ff_rule(
            "My-rule-3",
            ["src-2"],
            [],
            [],
            action="cascade",
            cascaded_rule_list="my-list",
        )
        with pytest.raises(AssertionError):
            assert bs.create_ff_rule(
                "My-rule-3", ["src-2"], [], [], action="dummy", placement="top"
            )
    assert len(responses.calls) == 3


@responses.activate
def test_ff_rule08():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/my-list?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_rule(
            "My-rule-3",
            ["src-2"],
            [],
            [],
            action="pass",
            placement="top",
            list="my-list",
        )
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule09():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/my-rule",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.delete_ff_rule("my-rule")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule10():
    responses.add(
        responses.DELETE,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/my-list/my-rule",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.delete_ff_rule("my-rule", "my-list")
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule11():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/my-list?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert bs.create_ff_rule(
            "My-rule-3",
            ["src-2"],
            [],
            [],
            action="custom",
            placement="top",
            list="my-list",
            custom_action_object={"type": "pass"},
        )
    assert len(responses.calls) == 1


@responses.activate
def test_ff_rule12():
    responses.add(
        responses.POST,
        "https://localhost:8443/rest/config/v1/forwarding-firewall/rules/lists/my-list?rcsMessage=added-via-REST-api",
        json={},
        status=204,
    )
    with pytest.raises(AssertionError):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert bs.create_ff_rule(
                "My-rule-3",
                ["src-2"],
                [],
                [],
                action="custom",
                placement="top",
                list="my-list",
            )
    assert len(responses.calls) == 0
