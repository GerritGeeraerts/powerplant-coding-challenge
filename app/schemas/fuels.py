"""Schemas for fuels data."""

from pydantic import BaseModel, Field

from app.core.config import settings


class FuelsIn(BaseModel):
    """Input schema for fuels data."""

    gas_price: float = Field(
        description="The price of gas per MWh in euros/MWh",
        examples=[13.4],
        ge=settings.MIN_FUEL_PRICE,
    )
    kerosine_price: float = Field(
        description="The price of kerosine per MWh in euros/MWh",
        examples=[50.8],
        ge=settings.MIN_FUEL_PRICE,
    )
    co2_price: float = Field(
        description="The price of CO2 emission certificates in euros/ton",
        examples=[20],
        ge=settings.MIN_FUEL_PRICE,
    )
    wind_percentage: float = Field(
        description="The percentage of wind turbine capacity that is available",
        examples=[60],
        ge=settings.MIN_WIND_PERCENTAGE,
        le=settings.MAX_WIND_PERCENTAGE,
    )

    @classmethod
    def validate_wind_percentage(cls, v: float) -> float:
        """Validate that wind percentage is within allowed range."""
        if v < settings.MIN_WIND_PERCENTAGE or v > settings.MAX_WIND_PERCENTAGE:
            raise ValueError(
                f"Wind percentage must be between {settings.MIN_WIND_PERCENTAGE} and {settings.MAX_WIND_PERCENTAGE}"
            )
        return v
