import sys
from collections import deque

input = sys.stdin.readline

T = int(input())

for _ in range(T):
    commands = input().strip()
    n = int(input())
    arr = deque()
    raw = sys.stdin.readline().strip()[1:-1]
    if raw:
        arr = deque(raw.split(","))
    else:
        arr = deque()
    index = 1
    error = False

    for command in commands:
        if command == "R":
            index *= -1
        if command == "D":
            if arr.__len__() == 0:
                print("error")
                error = True
                break
            if index == 1:
                arr.popleft()
            else:
                arr.pop()
                
                
    if not error:
        arr = list(map(int, arr))
        
        if index == -1:
            arr.reverse()
        output = '[' + ','.join(map(str, arr)) + ']'
        print(output)