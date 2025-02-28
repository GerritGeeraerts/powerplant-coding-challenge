"""Configuration settings for the application."""


from typing import List


class Settings:
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Power Plant Production API"
    PROJECT_DESCRIPTION: str = "API for calculating power plant production plans"

    # Power Plant Settings
    MIN_POWER_DECIMAL_PLACES: int = 1  # Number of decimal places for power values
    MAX_WIND_PERCENTAGE: float = 100.0
    MIN_WIND_PERCENTAGE: float = 0.0
    PRECISION: float = 0.1  # Precision for calculations

    MIN_FUEL_PRICE: float = 0.0

    ALLOWED_HOSTS: List[str] = ["*"]
    DEBUG: bool = True


settings = Settings()
