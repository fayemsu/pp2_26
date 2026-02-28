import datetime

x = datetime.datetime.now()

yest = x - datetime.timedelta(days = 1)
tmr = x + datetime.timedelta(days = 1)

print(yest.date())
print(x.date())
print(tmr.date())
