import datetime

class building:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'none')
        self.level = kwargs.get('level', 0)
        self.desired_level = kwargs.get('desired_level', 0)
        self.base_wood = kwargs.get('wood', 100)
        self.base_clay = kwargs.get('clay', 100)
        self.base_iron = kwargs.get('iron', 100)
        self.base_pop = kwargs.get('base_pop', 0)
        self.wood_factor = kwargs.get('wood_factor', 1.26)
        self.clay_factor = kwargs.get('clay_factor', 1.275)
        self.iron_factor = kwargs.get('iron_factor', 1.26)
        self.pop_factor = kwargs.get('pop_factor', 1.17)
        self.base_time = kwargs.get('base_time', datetime.timedelta(minutes=10))
        self.time_facto = kwargs.get('time_factor', 1.2)

    def set_id(self, id):
        self.id = id

    def resource_cost(self):
        pass

    def time(self):
        pass