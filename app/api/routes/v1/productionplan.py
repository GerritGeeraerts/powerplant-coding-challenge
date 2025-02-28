from typing import List

from fastapi import APIRouter

from app.models.meritorder import MeritOrder
from app.schemas.powerplant import PowerPlantOut
from app.schemas.productionplan import ProductionPlanIn
from app.utils import power_plant_factory

router = APIRouter()

@router.post('/', response_model=List[PowerPlantOut])
def production_plan(
        *,
        data: ProductionPlanIn
):
    """Calculate the production plan for a given load and a list of power plants"""
    power_plants = []
    for pp in data.powerplants:
        power_plants.append(power_plant_factory(pp, data.fuels))
    mo = MeritOrder(power_plants, data.load)
    mo.set_loads()
    return [{'name': pp.name, 'p': pp.p} for pp in mo.power_plants]
