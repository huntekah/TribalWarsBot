#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys, re
import csv
import datetime
from log_in import *
from village_info import village_info
import random


def builder_advanced(username, password, building):
    print("I will build", building)
    available = False
    while not available:
        driver = login(username, password)
        village = village_info(driver)
        current_building = village.buildings[building]
        if current_building.is_storage_needed:
            print("\t but first ", end="")
            builder_advanced(username, password, 'storage')
        if current_building.is_farm_needed:
            print("\t but first ", end="")
            builder_advanced(username, password, 'farm')
        available = current_building.available
        if (not current_building.is_farm_needed) and (not current_building.is_storage_needed) and (
                not current_building.available):
            alert_every_n_seconds(current_building.time, 999)
    row_name = "main_buildrow_{0}".format(building)
    driver.close()
    when = current_building.time + datetime.timedelta(seconds=random.randint(60, 180))
    build(row_name, when, username, password)
    driver.close()


if __name__ == "__main__":
    # builder_advanced("MałyPenis", "huntekah1", "main")

    try:
        with open('build_advanced.txt', 'r', encoding='utf-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for i, row in enumerate(spamreader):
                if i != 0:
                    building_id = row[0]

                    try:
                        builder_advanced(username, password, building_id)
                    except:
                        print(sys.exc_info())
                        print("had to omit")
                    print("\n\n")

                else:
                    pass
                    username = str(row[0]).strip()
                    password = str(row[1]).strip()
    except:
        print(sys.exc_info())
    finally:
        print("koniec")
