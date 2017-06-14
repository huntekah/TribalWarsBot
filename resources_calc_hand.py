DREWNO_SPEED = 1939
GLINA_SPEED = 1939
ZELAZO_SPEED = 1433


class Resource:
    def __init__(self, name, speed=None):
        self.name = name
        if speed == None:
            self.speed = int(input("Podaj produkcje " + self.name))
        else:
            self.speed = speed
        self.amount = int(input("Podaj zasoby " + self.name))
        self.cost = int(input("Podaj Koszt " + self.name))
        self.resource_time()

    def resource_time(self):
        self.time = float(self.cost - self.amount) / self.speed

    def __lt__(self, other):
        return self.time < other.time

    def read_cost(self):
        self.cost = int(input("Podaj Koszt " + self.name))
        self.resource_time()

class Market:
    def __init__(self, resources):
        self.resources = sorted(resources)

    def print_times(self):
        times = [(x.time * 60, x.name) for x in self.resources]
        for element in times:
            print("\tYou will have enough", element[1], "after", element[0], "minutes")

    def print_best_trades(self):
        total_speed = sum([x.speed for x in self.resources])
        total_amount = sum([x.amount for x in self.resources])
        total_cost = sum([x.cost for x in self.resources])
        total_time = float(total_cost - total_amount) / total_speed
        if self.resources[1].time < total_time:
            exchagnge1_amount = int((total_time - self.resources[0].time) * self.resources[0].speed)
            print("\tYou should exchange", exchagnge1_amount, self.resources[0].name, "for", self.resources[2].name)
            exchagnge1_amount = int((total_time - self.resources[1].time) * self.resources[1].speed)
            print("\tYou should exchange", exchagnge1_amount, self.resources[1].name, "for", self.resources[2].name)
            print("\tThis way you save %0.1f"% (60 * (self.resources[2].time - total_time)), "minutes")
        else:
            # exchagnge1_amount = int((total_time - self.resources[0].time) * self.resources[0].speed)
            needed_amount = abs((self.resources[2].amount + int((total_time) * self.resources[2].speed)) - self.resources[2].cost)
            print("\tYou should exchange", needed_amount, self.resources[0].name, "for", self.resources[2].name)
            needed_amount = abs((self.resources[1].amount + int((total_time) * self.resources[1].speed)) - self.resources[
                1].cost)
            print("\tYou should exchange", needed_amount, self.resources[0].name, "for", self.resources[1].name)
            print("\tThis way you save %0.1f" % (60 * (self.resources[2].time - total_time)), "minutes")

    def read_costs(self):
        self.resources.sort(key=lambda x: x.name)
        for resource in self.resources:
            resource.read_cost()
        self.resources.sort()

if __name__ == "__main__":
    drewno = Resource("drewno", DREWNO_SPEED)
    glina = Resource("glina", GLINA_SPEED)
    zelazo = Resource("zelazo", ZELAZO_SPEED)
    market = Market([drewno, glina, zelazo])
    condition = True
    while condition:
        market.print_times()
        market.print_best_trades()
        condition = (input("Sprawdzić inny budynek?(Y/N)") == "Y")
        if condition:
            market.read_costs()
