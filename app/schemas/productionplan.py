import logging
from typing import List
from pydantic import BaseModel, Field, field_validator

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn
from app.core.exceptions import InvalidLoadError
from app.core.config import settings

logger = logging.getLogger(__name__)

class ProductionPlanIn(BaseModel):
    """Input schema for production plan calculation"""
    load: float = Field(
        description='The load is the amount of energy (MWh) that need to be generated',
        example=400.1,
        ge=0
    )
    fuels: FuelsIn
    powerplants: List[PowerPlantIn]

    @field_validator('load')
    @classmethod
    def load_decimals(cls, v):
        """make sure that load is a multiple of settings.PRECISION"""
        # Check if the value is already a multiple of settings.PRECISION
        precision_factor = 1 / settings.PRECISION
        if round(v * precision_factor) != v * precision_factor:
            logger.warning(f"Load value {v} is not a multiple of {settings.PRECISION}")
            raise InvalidLoadError(v)
        logger.debug(f"Load value {v} validated")
        return v
