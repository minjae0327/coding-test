N, M = 3, 2

sequence = []

def backtrack():
    if len(sequence) == M:
        print(*sequence)
        return

    for i in range(1, N + 1):
        sequence.append(i)
        backtrack()
        sequence.pop()

backtrack()
