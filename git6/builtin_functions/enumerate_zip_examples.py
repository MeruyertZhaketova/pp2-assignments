names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# enumerate
for i, name in enumerate(names):
    print(i, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

# type checking
x = "123"
print(type(x))

# conversion
num = int(x)
print(num)