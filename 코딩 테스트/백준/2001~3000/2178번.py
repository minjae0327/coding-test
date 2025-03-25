from collections import deque

N, M = map(int, input().split())
board = [input() for _ in range(N)]
check_map = [[False for _ in range(M)] for _ in range(N)]

start_point = [0, 0]
check_map[start_point[0]][start_point[1]] = True

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 시작점과 함께 초기 비용(칸 수: 시작 위치 포함 1) 큐에 추가
have_to_visit = deque()
have_to_visit.append((start_point[0], start_point[1], 1))

def bfs():
    while have_to_visit:
        x, y, cost = have_to_visit.popleft()
        
        if x == N - 1 and y == M - 1:
            return cost
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < N and 0 <= ny < M:
                if board[nx][ny] == "1" and not check_map[nx][ny]:
                    check_map[nx][ny] = True
                    have_to_visit.append((nx, ny, cost + 1))
    return -1

print(bfs())