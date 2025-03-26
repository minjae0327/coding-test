import sys
from collections import deque

input = sys.stdin.readline
N = int(input())

queue = deque()
output = []

for _ in range(N):
    command = input().strip()

    if command.startswith("push"):
        _, x = command.split()
        queue.append(int(x))
    elif command == "pop":
        output.append(str(queue.popleft()) if queue else "-1")
    elif command == "size":
        output.append(str(len(queue)))
    elif command == "empty":
        output.append("1" if not queue else "0")
    elif command == "front":
        output.append(str(queue[0]) if queue else "-1")
    elif command == "back":
        output.append(str(queue[-1]) if queue else "-1")


sys.stdout.write("\n".join(output) + "\n")
