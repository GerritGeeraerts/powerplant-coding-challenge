import logging
from typing import List

from fastapi import APIRouter

from app.models.meritorder import MeritOrder
from app.schemas.powerplant import PowerPlantOut
from app.schemas.productionplan import ProductionPlanIn
from app.utils import power_plant_factory

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/', response_model=List[PowerPlantOut])
def production_plan(
        *,
        data: ProductionPlanIn
):
    """Calculate the production plan for a given load and a list of power plants"""
    logger.info(f"Calculating production plan for load {data.load} with {len(data.powerplants)} power plants")
    
    power_plants = []
    for pp in data.powerplants:
        logger.debug(f"Processing power plant: {pp.name} ({pp.type})")
        power_plants.append(power_plant_factory(pp, data.fuels))
    
    logger.debug(f"Created {len(power_plants)} power plant objects")
    mo = MeritOrder(power_plants, data.load)
    
    logger.info("Setting loads for power plants")
    mo.set_loads()
    
    result = [{'name': pp.name, 'p': pp.p} for pp in mo.power_plants]
    logger.info(f"Production plan calculation completed: {result}")
    return result
