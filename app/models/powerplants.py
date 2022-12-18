import abc

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn


class PowerPlant:
    def __init__(self, name, energy_effciency, pmin, pmax, fuelcost):
        self.name = name
        self.energy_effciency = energy_effciency  # Mw out / Mw in
        self.fuelcost = fuelcost  # euro / Mw
        self.cost_per_mw = fuelcost / energy_effciency  # euro / Mw
        self.pmin = pmin
        self.pmax = pmax
        self.real_pmin = pmin
        self.real_pmax = pmax
        self.p = 0

    def __repr__(self):
        return f'{self.name}'

    def __dict__(self):
        return {'name': self.name, 'p': self.p}

    @abc.abstractmethod
    def cost(self, load):
        pass


class WindTurbine(PowerPlant):
    def __init__(self, name, pmax, wind):
        super().__init__(name, 1, 0, pmax, 0)
        self.real_pmin = pmax * wind
        self.real_pmax = self.real_pmin

    def __dict__(self):
        return {'name': self.name, 'p': self.p}

    def cost(self, load):
        return 0


class Turbojet(PowerPlant):
    def cost(self, load):
        return load * self.fuelcost


class GasFired(PowerPlant):
    def cost(self, load):
        return load * self.fuelcost
