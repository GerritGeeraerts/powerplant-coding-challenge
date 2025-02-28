from app.core.config import settings

class InvalidLoadError(ValueError):
    """Exception raised when the load value is not a multiple of settings.PRECISION."""
    def __init__(self, value):
        self.value = value
        self.message = f"Load must be a multiple of {settings.PRECISION}, got {value}"
        super().__init__(self.message)
