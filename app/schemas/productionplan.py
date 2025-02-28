from typing import List
from pydantic import BaseModel, Field, field_validator

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn
from app.core.exceptions import InvalidLoadError


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
        """make sure that load is a multiple of 0.1"""
        # Check if the value is already a multiple of 0.1
        if round(v * 10) != v * 10:
            raise InvalidLoadError(v)
        return v
