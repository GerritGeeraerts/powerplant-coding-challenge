from app.models.powerplants import GasFired, Turbojet, WindTurbine
from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn


def power_plant_factory(pp: PowerPlantIn, fuels: FuelsIn):
    if pp.type == PowerPlantIn.Type.gasfired:
        return GasFired(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.gas_price)
    if pp.type == PowerPlantIn.Type.turbojet:
        return Turbojet(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.kerosine_price)
    if pp.type == PowerPlantIn.Type.windturbine:
        return WindTurbine(pp.name, pp.pmax, fuels.wind_rate, )
    assert False, 'unknown powerplant type'