import re

t = input()

x1 = re.match(r'ab*', t)

x2 = re.match(r'ab{2,3}', t)

x3 = re.findall(r'[a-z]+_[a-z]+', t)

x4 = re.findall(r'[A-Z][a-z]+', t)

x5 = re.match(r'a.*b', t)

x6 = re.sub(r'[\s.,]', ';', t)

x7 = re.sub(r'_([a-z])', lambda x: x.group(1).upper() , t)

x8 = re.findall('[A-Z][^A-Z]*', t)

x9 = re.sub(r'([A-Z])', lambda x: ' '+x.group(1), t)[1::]

x10 = re.sub(r'([A-Z])', lambda x: '_'+x.group(1).lower(), t)
