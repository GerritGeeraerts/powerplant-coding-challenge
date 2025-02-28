import logging
from app.models.powerplants import GasFired, Turbojet, WindTurbine
from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn

logger = logging.getLogger(__name__)

def power_plant_factory(pp: PowerPlantIn, fuels: FuelsIn):
    """
    Factory function to create a power plant object
    """
    logger.debug(f"Creating power plant of type {pp.type}: {pp.name}")
    
    if pp.type == PowerPlantIn.Type.gasfired:
        logger.debug(f"Creating GasFired plant with gas price: {fuels.gas_price}")
        return GasFired(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.gas_price)
    
    if pp.type == PowerPlantIn.Type.turbojet:
        logger.debug(f"Creating Turbojet plant with kerosine price: {fuels.kerosine_price}")
        return Turbojet(pp.name, pp.efficiency, pp.pmin, pp.pmax, fuels.kerosine_price)
    
    if pp.type == PowerPlantIn.Type.windturbine:
        logger.debug(f"Creating WindTurbine with wind rate: {fuels.wind_rate}")
        return WindTurbine(pp.name, pp.pmax, fuels.wind_rate)
    
    error_msg = f'Unknown powerplant type: {pp.type}'
    logger.error(error_msg)
    raise ValueError(error_msg)