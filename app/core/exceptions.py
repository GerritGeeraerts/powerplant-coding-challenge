"""Custom exceptions used throughout the application."""

from app.core.config import settings


class InvalidLoadError(ValueError):
    """Exception raised when the load value is not a multiple of settings.PRECISION."""

    def __init__(self, value: float) -> None:
        """Initialize with the invalid load value.

        Args:
            value: The invalid load value
        """
        self.value = value
        self.message = f"Load must be a multiple of {settings.PRECISION}, got {value}"
        super().__init__(self.message)


class InvalidPowerPlantTypeError(ValueError):
    """Exception raised when an unknown powerplant type is encountered."""

    def __init__(self, plant_type: str) -> None:
        """Initialize with the unknown plant type.

        Args:
            plant_type: The unknown power plant type
        """
        self.plant_type = plant_type
        self.message = f"Unknown powerplant type: {plant_type}"
        super().__init__(self.message)


class PmaxLessThanPminError(ValueError):
    """Exception raised when pmax is less than pmin for a power plant."""

    def __init__(self, pmax: float, pmin: float, plant_name: str | None = None) -> None:
        """Initialize with the invalid pmax and pmin values.

        Args:
            pmax: The maximum power value
            pmin: The minimum power value
            plant_name: Optional name of the power plant
        """
        self.pmax = pmax
        self.pmin = pmin
        self.plant_name = plant_name
        plant_info = f" for plant {plant_name}" if plant_name else ""
        self.message = f"pmax ({pmax}) must be greater than pmin ({pmin}){plant_info}"
        super().__init__(self.message)
