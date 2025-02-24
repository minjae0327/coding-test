def solution(dirs):
    direction = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0)
    }
    
    visited = set()
    
    # 현재 위치
    x, y = 0, 0
    
    for d in dirs:
        nx, ny = x + direction[d][0], y + direction[d][1]
        
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            # 길을 양방향으로 저장
            visited.add((x, y, nx, ny))  
            visited.add((nx, ny, x, y))
            x, y = nx, ny
    
    return len(visited) // 2
