from collections import deque

def solution(maps):
    # 방향 벡터 (상, 하, 좌, 우)
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    def bfs(end_x, end_y, maps):
        row, column = end_x + 1, end_y + 1
        have_to_visit = deque([(0, 0, 1)])
        visited = [[False] * column for _ in range(row)]
        visited[0][0] = True
        
        while have_to_visit:
            x, y, dist = have_to_visit.popleft()
            
            if (x, y) == (end_x, end_y):
                return dist
            
            #네 방항 탐색
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                
                # 범위 내에 있으며, 방분하지 않았고 갈 수 있다면
                if 0 <= nx < row and 0 <= ny < column \
                    and not visited[nx][ny] and maps[nx][ny] == 1:
                        have_to_visit.append((nx, ny, dist+1))
                        visited[nx][ny] = True
                    
        
        return -1
    
    return bfs(len(maps)-1, len(maps[0])-1, maps)
        