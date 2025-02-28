"""Production plan routes for the API."""

import logging
from typing import Dict, List, Union

from fastapi import APIRouter

from app.models.meritorder import MeritOrder
from app.models.powerplants import power_plant_factory
from app.schemas.productionplan import ProductionPlanIn

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=List[Dict[str, Union[str, float]]])  # type: ignore
async def production_plan(
    plan_input: ProductionPlanIn,
) -> List[Dict[str, Union[str, float]]]:
    """Calculate the production plan for the given input.

    Args:
        plan_input: The input data for the production plan calculation

    Returns:
        A list of power plants with their power output
    """
    # Create a merit order object
    power_plants = []
    for pp in plan_input.powerplants:
        power_plants.append(power_plant_factory(pp, plan_input.fuels))

    merit_order = MeritOrder(power_plants, plan_input.load)
    merit_order.set_loads()

    # Return the production plan
    return [pp.to_dict() for pp in merit_order.power_plants]
