class MeritOrder:
    """
    This class is used to calculate the merit order of a list of power plants
    """
    def __init__(self, power_plants, desired_load):
        """
        :param power_plants: List of power plants
        :param desired_load: The amount of energy (MWh) that need to be generated
        """
        self.power_plants = power_plants
        self.__sort_plants_by_cost_per_mw()
        self.desired_load = desired_load
        self.load = 0

    def __sort_plants_by_cost_per_mw(self):
        """
        Sort the power plants by cost per MW
        """
        self.power_plants.sort(key=lambda x: x.cost_per_mw)

    def set_loads(self):
        """
        Set the loads of the power plants for the most efficient production
        """
        for index, pp in enumerate(self.power_plants):
            if self.load + pp.real_pmax <= self.desired_load:
                # use real_pmax of powerplant
                self.load += pp.real_pmax
                self.power_plants[index].p = pp.real_pmax
                continue
            if self.load + pp.real_pmin > self.desired_load:
                # minimum of pp is too much, go back and reduce
                print(f'minimum is to much {self.load}+{pp.real_pmin} < {self.desired_load}')
                if index >= 1:
                    raise 'there is no previous powerplant to reduce'
                if self.power_plants[index - 1].p - pp.real_pmin > self.power_plants[index - 1].real_pmin:
                    raise 'the previous powerplant needs to be reduced to much'
                self.power_plants[index - 1].p = self.power_plants[index - 1].p - pp.real_pmin
                self.load -= pp.real_pmin
            self.power_plants[index].p = self.desired_load - self.load
            self.load = self.desired_load
            break
