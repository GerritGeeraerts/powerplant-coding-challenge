"""Schemas for power plants."""

import math
from enum import Enum

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from app.core.config import settings
from app.core.exceptions import PmaxLessThanPminError


class PowerPlantIn(BaseModel):
    """This is the input schema for a power plant. It is used to create a power plant object."""

    class Type(str, Enum):
        """Types of power plants."""

        gasfired = "gasfired"
        turbojet = "turbojet"
        windturbine = "windturbine"

    name: str = Field(
        examples=["gasfiredbig2"],
        description="This is the name of the power plant",
    )
    type: Type = Field(
        examples=[Type.gasfired],
        description="This is the type of the power plant",
    )
    efficiency: float = Field(
        examples=[0.53],
        ge=0,
        le=1,
        description="The efficiency at which they convert a MWh of fuel into a MWh of electrical energy. "
        'Wind-turbines do not consume "fuel", they generate power at zero price.',
    )
    pmin: float = Field(
        examples=[40.2],
        ge=0,
        description="The minimum amount of power the powerplant generates when switched on.",
        title="Minimum power",
    )
    pmax: float = Field(
        examples=[210.4],
        ge=0,
        title="Maximum power",
        description="the maximum amount of power the powerplant can generate",
    )

    @field_validator("pmax")
    @classmethod
    def pmin_le_pmax_decimals(cls, v: float, info: ValidationInfo) -> float:
        """Make sure pmax is bigger than pmin and convert pmax to a multiple of settings.PRECISION and le than pmax."""
        if "pmin" in info.data and v < info.data["pmin"]:
            raise PmaxLessThanPminError(v, info.data["pmin"], info.data.get("name"))
        precision_factor = 1 / settings.PRECISION
        return v * precision_factor // 1 / precision_factor

    @field_validator("pmin")
    @classmethod
    def pmin_decimals(cls, v: float) -> float:
        """Make sure that pmin is a multiple of settings.PRECISION and ge pmin."""
        precision_factor = 1 / settings.PRECISION
        return math.ceil(v * precision_factor) / precision_factor


class PowerPlantOut(BaseModel):
    """This is the output schema for a power plant. It is used to return the power plant object."""

    name: str = Field(
        examples=["gasfiredbig2"],
        description="The name of the power plant",
    )
    p: float = Field(
        examples=[200],
        description="The power that has to be produced by the power plant",
    )

    @field_validator("p")
    @classmethod
    def decimal(cls, v: float) -> float:
        """Fix the output to precision defined in settings."""
        return float(f"{{:0.{settings.MIN_POWER_DECIMAL_PLACES}f}}".format(v))
