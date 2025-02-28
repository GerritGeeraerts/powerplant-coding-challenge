"""Schemas for the application."""

from app.schemas.fuels import FuelsIn
from app.schemas.powerplant import PowerPlantIn, PowerPlantOut

__all__ = ["PowerPlantIn", "PowerPlantOut", "ProductionPlanIn", "FuelsIn"]

from app.schemas.productionplan import ProductionPlanIn
