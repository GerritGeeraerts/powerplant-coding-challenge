"""Merit order models for the application."""

import logging
from typing import List

from app.models.powerplants import PowerPlant

logger = logging.getLogger(__name__)


class MeritOrder:
    """This class is used to calculate the merit order of a list of power plants."""

    def __init__(self, power_plants: List[PowerPlant], desired_load: float) -> None:
        """
        Initialize the MeritOrder object.

        :param power_plants: List of power plants
        :param desired_load: The amount of energy (MWh) that need to be generated
        """
        self.power_plants = power_plants
        logger.info(
            f"Initializing MeritOrder with {len(power_plants)} power plants and desired load of {desired_load} MWh"
        )
        self.__sort_plants_by_cost_per_mw()
        self.desired_load = desired_load
        self.load = 0.0

    def __sort_plants_by_cost_per_mw(self) -> None:
        """Sort the power plants by cost per MW."""
        logger.debug("Sorting power plants by cost per MW")
        self.power_plants.sort(key=lambda x: x.cost_per_mw)
        logger.debug(f"Sorted order: {[pp.name for pp in self.power_plants]}")

    def set_loads(self) -> None:
        """Set the loads of the power plants for the most efficient production."""
        logger.info(
            f"Setting loads for power plants to meet desired load of {self.desired_load} MWh"
        )
        for index, pp in enumerate(self.power_plants):
            logger.debug(f"Processing plant {pp.name} (min: {pp.real_pmin}, max: {pp.real_pmax})")
            if self.load + pp.real_pmax <= self.desired_load:
                # use real_pmax of powerplant
                self.load += pp.real_pmax
                self.power_plants[index].p = pp.real_pmax
                logger.debug(
                    f"Set {pp.name} to max output {pp.real_pmax}, total load now {self.load}"
                )
                continue
            if self.load + pp.real_pmin > self.desired_load:
                # minimum of pp is too much, go back and reduce
                logger.warning(
                    f"Minimum output of {pp.name} ({pp.real_pmin}) is too much, current load: {self.load}, desired: {self.desired_load}"
                )
                if index >= 1:
                    error_msg = "There is no previous powerplant to reduce"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                if (
                    self.power_plants[index - 1].p - pp.real_pmin
                    > self.power_plants[index - 1].real_pmin
                ):
                    error_msg = "The previous powerplant needs to be reduced too much"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                prev_pp = self.power_plants[index - 1]
                new_output = prev_pp.p - pp.real_pmin
                logger.info(f"Reducing output of {prev_pp.name} from {prev_pp.p} to {new_output}")
                self.power_plants[index - 1].p = new_output
                self.load -= pp.real_pmin

            remaining_load = self.desired_load - self.load
            logger.info(f"Setting {pp.name} to {remaining_load} to meet remaining load")
            self.power_plants[index].p = remaining_load
            self.load = self.desired_load
            logger.info(f"Desired load of {self.desired_load} reached")
            break
