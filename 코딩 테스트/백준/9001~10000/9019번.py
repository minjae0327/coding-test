from collections import deque
import sys

input = sys.stdin.readline

cases = int(input())

def bfs(start, end):
    have_to_visit = deque()
    visited = [False] * 10000
    parent = [-1] * 10000    # 이전 상태 저장
    operator = [''] * 10000       # 어떤 연산으로 왔는지 저장

    have_to_visit.append(start)
    visited[start] = True

    while have_to_visit:
        current = have_to_visit.popleft()

        if current == end:
            break

        for op in ["D", "S", "L", "R"]:
            next_state = current
            
            if op == "D":
                next_state = (current * 2) % 10000
            elif op == "S":
                next_state = current - 1 if current != 0 else 9999
            elif op == "L":
                next_state = (current % 1000) * 10 + (current // 1000)
            elif op == "R":
                next_state = (current % 10) * 1000 + (current // 10)

            if not visited[next_state]:
                visited[next_state] = True
                parent[next_state] = current
                operator[next_state] = op
                have_to_visit.append(next_state)

    # 경로 복원
    result = []
    cur = end
    while cur != start:
        result.append(operator[cur])
        cur = parent[cur]

    return ''.join(reversed(result))


for _ in range(cases):
    start, end = map(int, input().split())
    print(bfs(start, end))
