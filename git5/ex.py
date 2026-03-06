import re

a="rain in spain"

x=re.search("^rain. *spain$", a)
y= re.findall("ai", a)
z= re.split("\s", a)
e= re.split("\s", a, 1)
i= re.sub("\s", "9", a)


print(x)
print(y)
print(z)
print(e)
print(i)


txt = "The rain in Spain"
o = re.search(r"\bS\w+", txt)
print(o.span())

o= re.search(r"\bS\w+", txt)
print(o.string)

o = re.search(r"\bS\w+", txt)
print(o.group())