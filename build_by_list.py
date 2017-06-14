#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys
import csv
from log_in import build
import datetime

try:
    with open('build_list.txt', 'r', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # username = spamreader[0, 0]
        # password = spamreader[0, 1]
        for i, row in enumerate(spamreader):
            if i != 0:
                building_id = row[0]
                month = int(row[1])
                day = int(row[2])
                hour = int(row[3])
                minute = int(row[4])
                second = int(row[5])
                t = datetime.datetime.today()
                when = datetime.datetime(t.year, month=month, day=day, hour=hour, minute=minute, second=second)
                print("user: {0}, password: {1}\n building: {2} \t time: {3}".format(username, password, building_id, when).encode('utf-8'))
                try:
                    build(building_id, when, username, password)
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
