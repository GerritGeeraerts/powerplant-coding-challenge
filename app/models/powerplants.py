import abc

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn


class PowerPlant:
    """Abstract class for power plants"""
    def __init__(self, name, energy_effciency, pmin, pmax, fuelcost):
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
        self.p = 0

    def __repr__(self):
        """Representation of the power plant object"""
        return f'{self.name}'

    def __str__(self):
        """explicit definition of the string representation of the power plant object"""
        return self.__repr__()

    def __dict__(self):
        """Representation of the power plant object as a dictionary"""
        return {'name': self.name, 'p': self.p}

    @abc.abstractmethod
    def cost(self, load):
        """this will be different and required for each type of power plant"""
        pass


class WindTurbine(PowerPlant):
    def __init__(self, name, pmax, wind):
        """for a wind turbine the real_pmin and real_pmax are the same and are calculated by the wind rate"""
        super().__init__(name, 1, 0, pmax, 0)
        self.real_pmin = pmax * wind
        self.real_pmax = self.real_pmin

    def __dict__(self):
        """Override the dict function for a wind turbine object"""
        return {'name': self.name, 'p': self.p}

    def cost(self, load):
        """cost calculation for a wind turbine, it is always free"""
        return 0


class Turbojet(PowerPlant):
    def cost(self, load):
        """cost calculation for a turbojet power plant"""
        return load * self.fuelcost


class GasFired(PowerPlant):
    def cost(self, load):
        """cost calculation for a gas fired power plant"""
        return load * self.fuelcost
