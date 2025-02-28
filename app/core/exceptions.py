class InvalidLoadError(ValueError):
    """Exception raised when the load value is not a multiple of 0.1."""
    def __init__(self, value):
        self.value = value
        self.message = f"Load must be a multiple of 0.1, got {value}"
        super().__init__(self.message)
