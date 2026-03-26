n=int(input())
x=list(map(int, input().split()))

cnt=0
even=list(filter(lambda i: i%2==0, x))

for i in even:
    cnt +=1
print(cnt)