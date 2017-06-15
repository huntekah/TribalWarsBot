#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import datetime


class village_info:
    def __init__(self, driver):
        self.driver = driver
        resource_speed = driver.find_element_by_xpath("//span[@id='wood']").get_attribute('title')
        self.wood_speed = int(re.findall('\d+', resource_speed)[0])
        print(resource_speed)
        resource_speed = driver.find_element_by_xpath("//span[@id='stone']").get_attribute('title')
        self.stone_speed = int(re.findall('\d+', resource_speed)[0])
        print(resource_speed)
        resource_speed = driver.find_element_by_xpath("//span[@id='iron']").get_attribute('title')
        self.iron_speed = int(re.findall('\d+', resource_speed)[0])
        print(resource_speed)

        self.wood_amount = int(re.findall('\d+', driver.find_element_by_xpath("//span[@id='wood']").text)[0])
        self.stone_amount = int(re.findall('\d+', driver.find_element_by_xpath("//span[@id='stone']").text)[0])
        self.iron_amount = int(re.findall('\d+', driver.find_element_by_xpath("//span[@id='iron']").text)[0])
        self.storage = int(re.findall('\d+', driver.find_element_by_xpath("//span[@id='storage']").text)[0])

        print("spichlerz: {0} | {1} | {2} / {3}".format(self.wood_amount, self.stone_amount, self.iron_amount,
                                                        self.storage))

        ### its important for drewno to be alphabetically first, glina second and zelazo third
        self.wood = Resource("drewno", self.wood_speed, self.wood_amount)
        self.stone = Resource("glina", self.stone_speed, self.stone_amount)
        self.iron = Resource("zelazo", self.iron_speed, self.iron_amount)

        self.market = Market([self.wood, self.stone, self.iron])

        self.population_current = int(
            re.findall('\d+', driver.find_element_by_xpath("//span[@id='pop_current_label']").text)[0])
        self.population_max = int(
            re.findall('\d+', driver.find_element_by_xpath("//span[@id='pop_max_label']").text)[0])
        print("Population: {0}/{1}".format(self.population_current,self.population_max))

        class building:
            def __init__(self, name, costs, duration, population, available, time, is_storage_needed, is_farm_needed,
                         next_lvl):
                self.name = name
                self.costs = costs
                self.duration = duration
                self.population = population
                self.available = available
                self.time = time
                self.is_storage_needed = is_storage_needed
                self.is_farm_needed = is_farm_needed
                self.next_lvl = next_lvl

            def __str__(self):
                string = "{0} \t costs: {1}\t duration: {2}\t population: {3} \t time: {4} \t next lvl: {5} \t available: {6} \t storage: {7} \t farm: {8}".format(
                    self.name, self.costs, self.duration, self.population, self.time, self.next_lvl, self.available, self.is_storage_needed, self.is_farm_needed)
                return string

        self.buildings = dict()
        id_list = driver.find_elements_by_xpath("//table[@id='buildings']//tr")
        #  //table[@id='buildings']//tr//span[@class='icon header time']/following-sibling::text()[1]   # times
        for id_driver in id_list:
            # print(id_driver.text)
            id = id_driver.get_attribute("id")
            if not id:
                continue
            name = id.replace("main_buildrow_", "")
            try:
                # resources
                wood_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_wood')]".format(id)
                wood_cost = int(driver.find_element_by_xpath(wood_string).get_attribute("data-cost"))
                stone_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_stone')]".format(id)
                stone_cost = int(driver.find_element_by_xpath(stone_string).get_attribute("data-cost"))
                iron_string = "//table[@id='buildings']//tr[@id='{0}']//td[contains(@class,'cost_iron')]".format(id)
                iron_cost = int(driver.find_element_by_xpath(iron_string).get_attribute("data-cost"))

                # print(id, "costs: {0} wood, {1} stone, {2} iron".format(wood_cost, stone_cost, iron_cost))

                # duration
                duration_string = "//table[@id='buildings']//tr[@id='{0}']//span[@class='icon header time']/..".format(
                    id)
                duration_text = driver.find_element_by_xpath(duration_string).text
                duration = self.time_text_to_time(duration_text)
                # print("duration: {0}".format( duration))

                # population //table[@id='buildings']//tr//span[@class='icon header population']/..
                if name != 'farm' and name != 'storage':
                    population_string = "//table[@id='buildings']//tr[@id='{0}']//span[@class='icon header population']/..".format(
                        id)
                    population = int(re.findall('\d+', driver.find_element_by_xpath(population_string).text)[0])
                else:
                    population = 0
                is_farm_needed = False
                is_storage_needed = False
                available = False
                if population + self.population_current > self.population_max:
                    is_farm_needed = True
                if max(wood_cost, stone_cost, iron_cost) > self.storage:
                    is_storage_needed = True

                if (not is_storage_needed) and (not is_farm_needed) and (wood_cost <= self.wood_amount)and (iron_cost <= self.iron_amount)and (stone_cost <= self.stone_amount):
                    available = True

                # build options
                build_options_string = "//table[@id='buildings']//tr[@id='{0}']//td[@class='build_options']".format(id)
                build_options = driver.find_element_by_xpath(build_options_string).get_attribute("textContent")
                lvl, when = self.process_build_options(build_options, look_for_when=(
                    (not available) and (not is_storage_needed) and (not is_farm_needed)))

                self.buildings[name] = building(name, costs=[wood_cost, stone_cost, iron_cost], duration=duration,
                                                population=population, is_storage_needed=is_storage_needed,
                                                is_farm_needed=is_farm_needed, available=available, next_lvl=lvl,
                                                time=when)

                print(self.buildings[name])
                print("\n")
            except:
                print(id)
                print(sys.exc_info())
                print("budynek w pełni rozbudowany\n\n")

    def resource_info(self):
        pass

    def time_text_to_time(self, time_text):
        time = [int(x) for x in time_text.split(':')]
        return datetime.timedelta(hours=time[0], minutes=time[1], seconds=time[2])

    def process_build_options(self, build_options, look_for_when):
        # print("\n\n",build_options,"\n\n")
        when = datetime.datetime.today()
        if build_options.find("Wybuduj") > -1:
            lvl = 1
        else:
            poziom = build_options.find("Poziom")
            if poziom == -1:
                raise Exception("There is no Wybuduj or Poziom, nie wiem co robic!")
            lvl = int(re.findall('\d+', build_options[poziom + len("Poziom"):])[0])
        if look_for_when:
            colon = build_options.find(":")
            hour = int(re.findall('\d+', build_options[colon - 2:colon])[0])
            minute = int(re.findall('\d+', build_options[colon + 1:colon + 3])[0])
            when = datetime.datetime(year=when.year, month=when.month, day=when.day, hour=hour, minute=minute,
                                     second=when.second)
            if when < datetime.datetime.today():
                when += datetime.timedelta(hours=24)
        return (lvl, when)


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
            if element[0] > 0:
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
