f = open("demofile.txt")
print(f.read())

with open("demofile.txt") as f:
  print(f.read())

with open("demofile.txt") as f:
  print(f.read(5))