#backjoon
import sys

N = int(sys.stdin.readline())

S = set()

for _ in range(N):
    command = (sys.stdin.readline().strip())

    if command.startswith("add"):
        _, x = command.split()
        S.add(int(x))
    elif command.startswith("remove"):
        _, x = command.split()
        S.discard(int(x))
    elif command.startswith("check"):
        _, x = command.split()
        if int(x) in S:
            print(1)
        else:
            print(0)
    elif command.startswith("toggle"):
        _, x = command.split()
        if int(x) in S:
            S.discard(int(x))
        else:
            S.add(int(x))
    elif command == "all":
        S = set(range(1, 21))
    elif command == "empty":
        S.clear()
