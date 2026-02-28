import datetime

x = datetime.datetime.now()

fda = x - datetime.timedelta(days = 5)

print(fda.date())


