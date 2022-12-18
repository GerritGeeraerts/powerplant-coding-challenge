from pprint import pprint
from typing import List

from fastapi import FastAPI, Body
from starlette.responses import RedirectResponse

from app.models.meritorder import MeritOrder
from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn, PowerPlantOut
from app.utils import power_plant_factory

app = FastAPI()


@app.get('/')
def redirect():
    response = RedirectResponse(url='/docs/')
    return response


@app.post('/productionplan/', response_model=List[PowerPlantOut])
def production_plan(
        *,
        load: float = Body(
            default=...,
            description='The load is the amount of energy (MWh) that need to be generated',
            example='400.1',
        ),
        fuels: FuelsIn,
        power_plants_in: List[PowerPlantIn] = Body(default=..., alias='powerplants', )
):
    power_plants = []
    for pp in power_plants_in:
        power_plants.append(power_plant_factory(pp, fuels))
    mo = MeritOrder(power_plants, load)
    mo.set_loads()
    return [{'name': pp.name, 'p': pp.p} for pp in mo.power_plants]
