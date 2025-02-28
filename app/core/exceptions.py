from app.core.config import settings

class InvalidLoadError(ValueError):
    """Exception raised when the load value is not a multiple of settings.PRECISION."""
    def __init__(self, value):
        self.value = value
        self.message = f"Load must be a multiple of {settings.PRECISION}, got {value}"
        super().__init__(self.message)

class InvalidPowerPlantTypeError(ValueError):
    """Exception raised when an unknown powerplant type is encountered."""
    def __init__(self, plant_type):
        self.plant_type = plant_type
        self.message = f"Unknown powerplant type: {plant_type}"
        super().__init__(self.message)

class PmaxLessThanPminError(ValueError):
    """Exception raised when pmax is less than pmin for a power plant."""
    def __init__(self, pmax, pmin, plant_name=None):
        self.pmax = pmax
        self.pmin = pmin
        self.plant_name = plant_name
        plant_info = f" for plant '{plant_name}'" if plant_name else ""
        self.message = f"pmax ({pmax}) must be greater than or equal to pmin ({pmin}){plant_info}"
        super().__init__(self.message)
