"""Schemas for production plan."""
import logging
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.core.config import settings
from app.core.exceptions import InvalidLoadError
from app.schemas import FuelsIn, PowerPlantIn

logger = logging.getLogger(__name__)


class ProductionPlanIn(BaseModel):
    """Input schema for production plan calculation."""

    load: float = Field(
        ...,
        description="The load is the amount of energy (MWh) that need to be generated",
        examples=[400.1],
        ge=0,
    )
    fuels: FuelsIn
    powerplants: List[PowerPlantIn]

    @field_validator("load")
    @classmethod
    def load_decimals(cls, v: float) -> float:
        """Make sure that load is a multiple of settings.PRECISION."""
        # Check if the value is already a multiple of settings.PRECISION
        precision_factor = 1 / settings.PRECISION
        if round(v * precision_factor) != v * precision_factor:
            logger.warning(f"Load {v} is not a multiple of {settings.PRECISION}, will be rejected")
            raise InvalidLoadError(v)
        return v
