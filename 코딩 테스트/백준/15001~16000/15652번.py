N, M = map(int, input().split())

sequence = []

def backtrack():
    if len(sequence) == M:
        print(*sequence)
        return

    for i in range(1, N + 1):
        if len(sequence) == 0:
            sequence.append(i)
        elif i < sequence[-1]:
            continue
        else:
            sequence.append(i)
        backtrack()
        sequence.pop()

backtrack()
