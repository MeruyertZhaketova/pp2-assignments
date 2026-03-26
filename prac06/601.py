n=int(input())

x=list(map(int, input().split()))

s=sum(map(lambda i: i**2, x))

print(s)