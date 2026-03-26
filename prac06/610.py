n = int(input())
numbers = map(int, input().split())

count = sum(map(bool, numbers))

print(count)