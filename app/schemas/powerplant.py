from enum import Enum

from pydantic import validator, Field, BaseModel


class PowerPlantIn(BaseModel):
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
        if 'pmin' in values and v < values['pmin']:
            raise ValueError('pmax has to be higher or equal to pmin')
        return v


class PowerPlantOut(BaseModel):
    pass
