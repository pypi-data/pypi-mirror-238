import responses
import pytest
from barracuda_api.barracuda import BarracudaSession

get_box_info = {
    "appliance": "VM",
    "cpuCores": 1,
    "cpuLoad": {
        "minute1": 0.07000000029802322,
        "minute15": 0.019999999552965164,
        "minute5": 0.07999999821186066,
    },
    "hostname": "CloudGen-Firewall",
    "hypervisor": "VMWare",
    "isdiskencrypted": False,
    "memory": {"free": 3216, "total": 3936, "usage": 18, "used": 720},
    "model": "vf1000",
    "release": "GWAY-8.3.1-0086",
    "serialNumber": "",
    "time": "Mon Jul 11 14:58:05 2022",
    "timezone": "Etc/UTC",
    "uptime": 287721,
    "users": 0,
}


@responses.activate
def test_box_info_01():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/control/v1/box/info",
        json=get_box_info,
        status=200,
    )
    with BarracudaSession("localhost", "this-is-a-very-secret-token", debug=True) as bs:
        assert "appliance" in bs.get_box_info()
        assert bs.base_url == "https://localhost:8443"
    assert len(responses.calls) == 1


@responses.activate
def test_box_info_02():
    with BarracudaSession(
        "localhost", "this-is-a-very-secret-token", endpoint_port=1234, debug=True
    ) as bs:
        assert bs.base_url == "https://localhost:1234"


@responses.activate
def test_box_info_03():
    responses.add(
        responses.GET,
        "https://localhost:8443/rest/control/v1/box/info",
        json=get_box_info,
        status=400,
    )
    with pytest.raises(Exception):
        with BarracudaSession(
            "localhost", "this-is-a-very-secret-token", debug=True
        ) as bs:
            assert "appliance" in bs.get_box_info()
    assert len(responses.calls) == 1
