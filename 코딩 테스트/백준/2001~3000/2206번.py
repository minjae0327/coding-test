from collections import deque

def bfs():
    while have_to_visit:
        x, y, cost, pass_wall = have_to_visit.popleft()
        
        if x == N - 1 and y == M - 1:
            return cost
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < N and 0 <= ny < M:
                # 벽을 통과할 때
                if board[nx][ny] == "1" and pass_wall == 0 and not visited[nx][ny][1]:
                    visited[nx][ny][1] = True
                    have_to_visit.append((nx, ny, cost + 1, 1))
                # 벽을 통과하지 않았을 때
                elif board[nx][ny] == "0" and not visited[nx][ny][pass_wall]:
                    visited[nx][ny][pass_wall] = True
                    have_to_visit.append((nx, ny, cost + 1, pass_wall))
                        
    return -1


N, M = map(int, input().split())
board = [input() for _ in range(N)]
visited = [[[False] * 2 for _ in range(M)] for _ in range(N)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

pass_wall = 0

have_to_visit = deque()
have_to_visit.append((0, 0, 1, pass_wall))
visited[0][0][0] = True

print(bfs())