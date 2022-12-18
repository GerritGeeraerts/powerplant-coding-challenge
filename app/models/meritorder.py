class MeritOrder:
    def __init__(self, power_plants, desired_load):
        self.power_plants = power_plants
        self.__sort_plants_by_cost_per_mw()
        self.desired_load = desired_load
        self.load = 0

    def __sort_plants_by_cost_per_mw(self):
        self.power_plants.sort(key=lambda x: x.cost_per_mw)

    def set_loads(self):
        for index, pp in enumerate(self.power_plants):
            if self.load + pp.real_pmax <= self.desired_load:
                # use real_pmax of powerplant
                self.load += pp.real_pmax
                self.power_plants[index].p = pp.real_pmax
                # breakpoint()
                continue
            if self.load + pp.real_pmin > self.desired_load:
                # minimum of pp is too much, go back and reduce
                print(f'minimum is to much {self.load}+{pp.real_pmin} < {self.desired_load}')
                assert index >= 1, 'there is no previous powerplant to reduce'
                # breakpoint()
                assert self.power_plants[index - 1].p - pp.real_pmin > self.power_plants[index - 1].real_pmin, \
                    'the previous powerplant needs to be reduced to much'
                self.power_plants[index - 1].p = self.power_plants[index - 1].p - pp.real_pmin
                self.load -= pp.real_pmin
            self.power_plants[index].p = self.desired_load - self.load
            self.load = self.desired_load
            # breakpoint()
            break
