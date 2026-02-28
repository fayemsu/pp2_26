import datetime

x = input('"YYYY-MM-DD HH:MM:SS":')
y = input('"YYYY-MM-DD HH:MM:SS":')

x = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
y = datetime.datetime.strptime(y, "%Y-%m-%d %H:%M:%S")

print((y-x).total_seconds())