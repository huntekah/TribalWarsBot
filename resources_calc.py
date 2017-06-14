from log_in import *
import re
import sys


class Resource:
    def __init__(self, name, speed, amount, cost=0):
        self.name = name
        self.speed = speed
        self.amount = amount
        self.cost = cost
        self.resource_time()

    def resource_time(self):
        self.time = float(self.cost - self.amount) / self.speed

    def __lt__(self, other):
        self.resource_time()
        return self.time < other.time

    def set_cost(self, cost):
        self.cost = cost
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
            print("\tThis way you save %0.1f" % (60 * (self.resources[2].time - total_time)), "minutes")
        else:
            # exchagnge1_amount = int((total_time - self.resources[0].time) * self.resources[0].speed)
            needed_amount = abs(
                (self.resources[2].amount + int((total_time) * self.resources[2].speed)) - self.resources[2].cost)
            print("\tYou should exchange", needed_amount, self.resources[0].name, "for", self.resources[2].name)
            needed_amount = abs(
                (self.resources[1].amount + int((total_time) * self.resources[1].speed)) - self.resources[
                    1].cost)
            print("\tYou should exchange", needed_amount, self.resources[0].name, "for", self.resources[1].name)
            print("\tThis way you save %0.1f" % (60 * (self.resources[2].time - total_time)), "minutes")

    def set_costs(self, cost_list):
        self.resources.sort(key=lambda x: x.name)
        for resource, cost in zip(self.resources, cost_list):
            # print("updating {0} with cost {1}".format(resource.name, cost))
            resource.set_cost(cost)
        self.resources.sort()


def get_all_trades():
    driver = login()
    resource_speed = driver.find_element_by_xpath("//table[@class='box smallPadding']//span[@id='wood']").get_attribute(
        'title')
    wood_speed = int(re.findall('\d+', resource_speed)[0])
    print(resource_speed)
    resource_speed = driver.find_element_by_xpath(
        "//table[@class='box smallPadding']//span[@id='stone']").get_attribute('title')
    stone_speed = int(re.findall('\d+', resource_speed)[0])
    print(resource_speed)
    resource_speed = driver.find_element_by_xpath("//table[@class='box smallPadding']//span[@id='iron']").get_attribute(
        'title')
    iron_speed = int(re.findall('\d+', resource_speed)[0])
    print(resource_speed)

    wood_amount = int(
        re.findall('\d+', driver.find_element_by_xpath("//table[@class='box smallPadding']//span[@id='wood']").text)[0])
    stone_amount = int(
        re.findall('\d+', driver.find_element_by_xpath("//table[@class='box smallPadding']//span[@id='stone']").text)[
            0])
    iron_amount = int(
        re.findall('\d+', driver.find_element_by_xpath("//table[@class='box smallPadding']//span[@id='iron']").text)[0])

    print("spichlerz: {0} | {1} | {2}".format(wood_amount, stone_amount, iron_amount))

### its important for drewno to be alphabetically first, glina second and zelazo third
    wood = Resource("drewno", wood_speed, wood_amount)
    stone = Resource("glina", stone_speed, stone_amount)
    iron = Resource("zelazo", iron_speed, iron_amount)

    market = Market([wood, stone, iron])

    id_list = driver.find_elements_by_xpath("//table[@id='buildings']//tr")

    for id_driver in id_list:
        print(id_driver.text)
        id = id_driver.get_attribute("id")
        if not id:
            continue
        try:
            wood_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_wood')]".format(id)
            wood_cost = int(driver.find_element_by_xpath(wood_string).get_attribute("data-cost"))
            stone_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_stone')]".format(id)
            stone_cost = int(driver.find_element_by_xpath(stone_string).get_attribute("data-cost"))
            iron_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_iron')]".format(id)
            iron_cost = int(driver.find_element_by_xpath(iron_string).get_attribute("data-cost"))
            print(id, "costs: {0} wood, {1} stone, {2} iron".format(wood_cost, stone_cost, iron_cost))
            market.set_costs([wood_cost, stone_cost, iron_cost])
            market.print_times()
            market.print_best_trades()
            print("\n\n")
        except:
            print(id)
            print(sys.exc_info()[0])
            print("budynek w pełni ozbudowany\n\n")


if __name__ == "__main__":
    get_all_trades()
    pass
    # drewno = Resource("drewno", DREWNO_SPEED)
    # glina = Resource("glina", GLINA_SPEED)
    # zelazo = Resource("zelazo", ZELAZO_SPEED)
    # market = Market([drewno, glina, zelazo])
    # condition = True
    # while condition:
    #     market.print_times()
    #     market.print_best_trades()
    #     condition = (input("Sprawdzić inny budynek?(Y/N)") == "Y")
    #     if condition:
    #         market.read_costs()
