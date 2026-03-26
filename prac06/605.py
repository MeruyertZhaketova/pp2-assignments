"""s=input()

cnt=0
v="aeiouAEIOU"

for c in s:
    if c in v:
        cnt+=1
print(cnt)"""

s = input()

vowels = "aeiouAEIOU"

if any(c in vowels for c in s):
    print("Yes")
else:
    print("No")
