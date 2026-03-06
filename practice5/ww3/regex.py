import re


txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)



'''
findall	 Returns a list containing all matches
search	 Returns a Match object if there is a match anywhere in the string
split	 Returns a list where the string has been split at each match
sub	     Replaces one or many matches with a string
'''

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

txt = "The rain in Spain"
x = re.findall("Portugal", txt)
print(x)



x = re.search("\s", txt)
print(x)
print("The first white-space character is located in position:", x.start())


txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)

import re

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)


txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)


txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)


print("")


txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) #this will print an object
print(x.span())
print(x.string)
print(x.group())



x = re.search(r"\bS\w+", txt)
print(x) #this will print an object
print(x.span())
print(x.string)
print(x.group())