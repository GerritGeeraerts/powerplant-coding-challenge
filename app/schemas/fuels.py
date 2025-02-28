from pydantic import BaseModel, Field, field_validator
from app.core.config import settings


class FuelsIn(BaseModel):
    gas_price: float = Field(
        alias="gas(euro/MWh)",
        example=1.1,
        ge=settings.MIN_FUEL_PRICE,
        description='The price (EUR) of gas per MWh'
    )
    kerosine_price: float = Field(
        alias="kerosine(euro/MWh)",
        example=2.25,
        ge=0,
        description='The price (EUR) of kerosine per MWh',
    )
    co2_price: float = Field(
        alias="co2(euro/ton)",
        example=1,
        ge=0,
        description='The price of emission allowances',
    )
    wind_rate: float = Field(
        alias="wind(%)",
        example=75,
        ge=settings.MIN_WIND_PERCENTAGE,
        le=settings.MAX_WIND_PERCENTAGE,
        description='Percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with '
                    'a Pmax of 4 MW will generate 1MWh of energy.',
    )

    @field_validator('wind_rate')
    @classmethod
    def decimals(cls, v):
        """Recalculate the wind rate to a percentage"""
        return v / 100
