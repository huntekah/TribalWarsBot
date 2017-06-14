import datetime

production = [530,616,717,833,969,1127,1311,1525,1774,2063]
times = [107071]

wood = 126898 + 28000 + 40000
stone = 139161 + 30000+50000
iron = 121303 +25000+50000
t = datetime.timedelta(hours=64,minutes=41,seconds=37)
now = datetime.datetime.today()
print(now < (now+t))
print((wood/t.total_seconds())*3600)
print((stone/t.total_seconds())*3600)
print((iron/t.total_seconds())*3600)

while True:
    hour = int(input("hour"))
    minute = int(input("minute"))
    second = int(input("second"))
    print(datetime.timedelta(hours=hour,minutes=minute,seconds=second).total_seconds())


day = int(input("day"))
hour = int(input("hour"))
minute = int(input("minute"))
second = int(input("second"))
t = datetime.datetime.today()
when = datetime.datetime(t.year, month=t.month, day=day, hour=hour, minute=minute, second=second)
print(when)

while True:
    hour = int(input("hour"))
    minute = int(input("minute"))
    second = int(input("second"))
    delta = datetime.timedelta(hours=hour,minutes=minute,seconds=second)
    when += delta
    print("main_buildrow_", when)


