import sys

input = sys.stdin.readline

n = int(input())
m = int(input())
loc = 0
answer = 0
count = 0

s = input().strip()

compare = "IOI" 

i = 0
while i < m - 1:
    if s[i:i+3] == compare:
        count += 1
        i += 2
        if count == n:
            count -=1
            answer += 1
    else:
        i += 1
        count = 0

print(answer)