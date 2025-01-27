import math
from enum import Enum

from pydantic import validator, Field, BaseModel


class PowerPlantIn(BaseModel):
    """This is the input schema for a power plant. It is used to create a power plant object."""
    class Type(str, Enum):
        gasfired = "gasfired"
        turbojet = "turbojet"
        windturbine = "windturbine"

    name: str = Field(
        example='gasfiredbig2',
        description='This is the name of the power plant',
    )
    type: Type = Field(
        example=Type.gasfired,
        description='This is the type of the power plant',
    )
    efficiency: float = Field(
        example=0.53,
        ge=0,
        le=1,
        description='The efficiency at which they convert a MWh of fuel into a MWh of electrical energy. '
                    'Wind-turbines do not consume "fuel", they generate power at zero price.',
    )
    pmin: float = Field(
        example=40.2,
        ge=0,
        description='The minimum amount of power the powerplant generates when switched on.',
        title='Minimum power',
    )
    pmax: float = Field(
        example=210.4,
        ge=0,
        title='Maximum power',
        description='the maximum amount of power the powerplant can generate',
    )

    @validator('pmax')
    def pmin_le_pmax_decimals(cls, v, values, **kwargs):
        """make sure pmax is bigger than pmin and convert pmax to a multiple of 0.1 and le than pmax"""
        if 'pmin' in values and v < values['pmin']:
            raise ValueError('pmax has to be higher or equal to pmin')
        return v*10//1/10

    @validator('pmin')
    def pmin_decimals(cls, v):
        """make sure that pmin is a multiple of 0.1 and ge pmin"""
        return math.ceil(v*10)/10


class PowerPlantOut(BaseModel):
    """This is the output schema for a power plant. It is used to return the power plant object."""
    name: str = Field(
        example='gasfiredbig2',
        description='The name of the power plant',
    )
    p: float = Field(
        example=200,
        description='The power that has to be produced by the power plant',
    )

    @validator('p')
    def decimal(cls, v):
        """fix the output to one decimal"""
        return float('{:0.1f}'.format(v))
