"""Power plant models for production planning."""

import logging
from typing import Any, Dict

from app.core.exceptions import InvalidPowerPlantTypeError
from app.schemas import FuelsIn, PowerPlantIn

logger = logging.getLogger(__name__)


class PowerPlant:
    """Abstract class for power plants."""

    def __init__(
        self, name: str, energy_effciency: float, pmin: float, pmax: float, fuelcost: float
    ) -> None:
        """Initialize a power plant.

        Args:
            name: Name of the power plant
            energy_effciency: Efficiency at which the plant converts fuel to energy
            pmin: Minimum power output
            pmax: Maximum power output
            fuelcost: Cost of fuel per MWh
        """
        self.name = name
        self.energy_effciency = energy_effciency  # Mw out / Mw in
        self.fuelcost = fuelcost  # euro / Mw
        # calculate the cost per Mw
        self.cost_per_mw = fuelcost / energy_effciency  # euro / Mw
        self.pmin = pmin
        self.pmax = pmax
        # real_pmin and real_pmax are used to calculate the real minimum and maximum power output of a power plant
        self.real_pmin = pmin
        self.real_pmax = pmax
        # set the power output to 0 by default
        self.p = 0.0
        logger.debug(
            f"Created {self.__class__.__name__} '{name}' with efficiency {energy_effciency}, pmin {pmin}, pmax {pmax}"
        )

    def __repr__(self) -> str:
        """Return string representation of the power plant.

        Returns:
            String representation
        """
        return f"{self.name}"

    def __str__(self) -> str:
        """Return string representation of the power plant.

        Returns:
            String representation
        """
        return self.__repr__()

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation of the power plant.

        Returns:
            Dictionary with name and power output
        """
        return {"name": self.name, "p": self.p}

    def cost(self, load: float) -> float:
        """Calculate the cost for a given load.

        Args:
            load: The power output in MW

        Returns:
            The cost in euros
        """
        raise NotImplementedError("Subclasses must implement this method")


class WindTurbine(PowerPlant):
    """Wind turbine power plant."""

    def __init__(self, name: str, pmax: float, wind_percentage: float) -> None:
        """Initialize a wind turbine power plant.

        Args:
            name: Name of the power plant
            pmax: Maximum power output
            wind_percentage: Percentage of wind availability (0-100)
        """
        # Wind turbines have 100% efficiency, 0 fuel cost, and pmin of 0
        super().__init__(name, 1.0, 0.0, pmax, 0.0)
        # Adjust real_pmax based on wind availability
        self.real_pmax = pmax * (wind_percentage / 100.0)

    def cost(self, load: float) -> float:
        """Cost calculation for a wind turbine.

        Wind turbines have zero fuel cost.

        Args:
            load: The power output in MW

        Returns:
            Always 0 as wind turbines have no fuel cost
        """
        logger.debug(f"Calculating cost for wind turbine '{self.name}' with load {load}: 0")
        return 0


class TurboJet(PowerPlant):
    """Turbo jet power plant."""

    def cost(self, load: float) -> float:
        """Cost calculation for a turbo jet power plant.

        Args:
            load: The power output in MW

        Returns:
            The cost in euros
        """
        logger.debug(
            f"Calculating cost for turbo jet plant '{self.name}' with load {load}: {load * self.fuelcost}"
        )
        return load * self.fuelcost


class GasFired(PowerPlant):
    """Gas fired power plant."""

    def cost(self, load: float) -> float:
        """Cost calculation for a gas fired power plant.

        Args:
            load: The power output in MW

        Returns:
            The cost in euros
        """
        logger.debug(
            f"Calculating cost for gas fired plant '{self.name}' with load {load}: {load * self.fuelcost}"
        )
        return load * self.fuelcost


def power_plant_factory(pp: PowerPlantIn, fuels: FuelsIn) -> PowerPlant:
    """Create a power plant object based on the input parameters.

    Args:
        pp: Power plant input schema
        fuels: Fuels input schema

    Returns:
        A PowerPlant instance of the appropriate type

    Raises:
        InvalidPowerPlantTypeError: If the power plant type is unknown
    """
    logger.debug(f"Creating power plant of type {pp.type}: {pp.name}")

    if pp.type == PowerPlantIn.Type.gasfired:
        logger.debug(f"Creating GasFired plant with gas price: {fuels.gas_price}")
        return GasFired(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.gas_price)

    if pp.type == PowerPlantIn.Type.turbojet:
        logger.debug(f"Creating Turbojet plant with kerosine price: {fuels.kerosine_price}")
        return TurboJet(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.kerosine_price)

    if pp.type == PowerPlantIn.Type.windturbine:
        logger.debug(f"Creating WindTurbine with wind rate: {fuels.wind_percentage}")
        return WindTurbine(pp.name, pp.pmax, fuels.wind_percentage)

    error_msg = f"Unknown powerplant type: {pp.type}"
    logger.error(error_msg)
    raise InvalidPowerPlantTypeError(pp.type)
