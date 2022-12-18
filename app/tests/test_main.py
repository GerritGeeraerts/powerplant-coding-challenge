import json

from fastapi.testclient import TestClient
from fastapi import status

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn


def test_production_plan_not_accept_http_methods(client: TestClient):
    """
    Do not accept 'put', 'delete', 'options', 'head', 'patch' methods for the /productionplan/ endpoint
    """
    not_allowed_methods = ['put', 'delete', 'options', 'head', 'patch', ]
    for na_method in not_allowed_methods:
        response = getattr(client, na_method)('/productionplan/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, f'{na_method} should be not allowed'


def test_production_plan_accept_http_post(client: TestClient):
    """test that the endpoint (/productionplan/) accepts HTTP post """
    response = client.post('/productionplan/')
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_fuels_schema():
    fuels = {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 60
    }
    result = FuelsIn(**fuels)
    assert result.gas_price == 13.4
    assert result.kerosine_price == 50.8
    assert result.co2_price == 20
    assert result.wind_rate == 0.6


def test_powerplant_type_gasfired():
    power_plant = {
        "name": "gasfiredbig1",
        "type": "gasfired",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460
    }
    result = PowerPlantIn(**power_plant)
    assert result.type == 'gasfired'


def test_powerplant_type_turbojet():
    power_plant = {
        "name": "gasfiredbig1",
        "type": "turbojet",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460
    }
    result = PowerPlantIn(**power_plant)
    assert result.type == 'turbojet'


def test_powerplant_type_windturbine():
    power_plant = {
        "name": "gasfiredbig1",
        "type": "windturbine",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460
    }
    result = PowerPlantIn(**power_plant)
    assert result.type == 'windturbine'


def test_powerplant_type_no_free_type():
    """test that the powerplant type does not accept free text"""
    # todo
    pass


def test_powerplant_pmin_decimals():
    """convert pmin to a multiple of 0.1 for pmin 100.12 it should be converted to 100.2"""
    power_plant = {"name": "", "type": "windturbine", "efficiency": 0.53, "pmin": 100.12, "pmax": 460}
    result = PowerPlantIn(**power_plant)
    assert result.pmin == 100.2


def test_powerplant_pmax_decimals():
    """convert pmax to a multiple of 0.1 for pmax 460.14 it should be converted to 460.1"""
    power_plant = {"name": "", "type": "windturbine", "efficiency": 0.53, "pmin": 100, "pmax": 460.14}
    result = PowerPlantIn(**power_plant)
    assert result.pmax == 460.1


def test_power_plant_schema():
    power_plant = {
        "name": "gasfiredbig1",
        "type": "gasfired",
        "efficiency": 0.53,
        "pmin": 100,
        "pmax": 460
    }
    result = PowerPlantIn(**power_plant)
    assert result.name == "gasfiredbig1"
    assert result.type == "gasfired"
    assert result.efficiency == 0.53
    assert result.pmin == 100
    assert result.pmax == 460


def test_basic_pay_load(client: TestClient):
    """
    With a load of 0 and no power plants the production plan should be an empty list
    """
    response = client.post(
        '/productionplan/',
        json={
            "load": 0,
            "fuels":
                {
                    "gas(euro/MWh)": 13.4,
                    "kerosine(euro/MWh)": 50.8,
                    "co2(euro/ton)": 20,
                    "wind(%)": 60
                },
            "powerplants": [],
        })
    assert response.json() == []


def test_main_payload_1(client: TestClient):
    """
    test the '/productionplan/' with the example payload1.json data
    """
    with open('./example_payloads/payload1.json') as f:
        payload = json.load(f)
        response = client.post(
            '/productionplan/',
            json=payload,
        )
        result = response.json()

        result_d = {}
        for dict_ in result:
            result_d[dict_['name']] = dict_['p']

        # breakpoint()
        assert result_d['windpark1'] == 90.0
        assert result_d['windpark2'] == 21.6
        assert result_d['gasfiredbig1'] + result_d['gasfiredbig2'] == 368.4
        assert 100 <= result_d['gasfiredbig1'] <= 460 or result_d['gasfiredbig1'] == 0
        assert 100 <= result_d['gasfiredbig2'] <= 460 or result_d['gasfiredbig2'] == 0
        assert result_d['gasfiredsomewhatsmaller'] == 0
        assert result_d['tj1'] == 0


def test_main_payload_2(client: TestClient):
    """
    test the '/productionplan/' with the example payload2.json data
    """
    with open('./example_payloads/payload2.json') as f:
        payload = json.load(f)
        response = client.post(
            '/productionplan/',
            json=payload,
        )
        result = response.json()

        result_d = {}
        for dict_ in result:
            result_d[dict_['name']] = dict_['p']

        assert result_d['windpark1'] == 0
        assert result_d['windpark2'] == 0
        assert result_d['gasfiredbig1'] + result_d['gasfiredbig2'] == 480
        assert 100 <= result_d['gasfiredbig1'] <= 460 or result_d['gasfiredbig1'] == 0
        assert 100 <= result_d['gasfiredbig2'] <= 460 or result_d['gasfiredbig2'] == 0
        assert result_d['gasfiredsomewhatsmaller'] == 0
        assert result_d['tj1'] == 0


def test_main_payload_3(client: TestClient):
    """
    test the '/productionplan/' with the example payload3.json data
    """
    with open('./example_payloads/payload3.json') as f:
        payload = json.load(f)
        response = client.post(
            '/productionplan/',
            json=payload,
        )
        result = response.json()

        result_d = {}
        for dict_ in result:
            result_d[dict_['name']] = dict_['p']

        assert result_d['windpark1'] == 90.0
        assert result_d['windpark2'] == 21.6
        assert result_d['gasfiredbig1'] + result_d['gasfiredbig2'] == 798.4
        assert 100 <= result_d['gasfiredbig1'] <= 460 or result_d['gasfiredbig1'] == 0
        assert 100 <= result_d['gasfiredbig2'] <= 460 or result_d['gasfiredbig2'] == 0
        assert result_d['gasfiredsomewhatsmaller'] == 0
        assert result_d['tj1'] == 0
