def solution(park, routes):
    def get_loc(park, start, fix, move, max_size, reverse=False):
        origin_start = start
        
        step = 1
        if reverse:
            step *= -1
        
        for i in range(move):
            start += step
            if start < 0 or start >= max_size:
                return origin_start
            if (fix == 'x' and park[start][origin_fix] == -1) or (fix == 'y' and park[origin_fix][start] == -1):
                return origin_start
            
        return start

    # 공원 지도 생성
    park_list = []
    x = 0
    y = 0

    max_x = len(park)       # 행의 크기
    max_y = len(park[0])    # 열의 크기

    for j in range(max_x):
        row = []
        for i in range(max_y):
            if park[j][i] == 'S':
                x = j
                y = i
            if park[j][i] != 'X':
                row.append(0)
            else:
                row.append(-1)
        park_list.append(row)

    # 이동 명령 처리
    for route in routes:
        direct, count = route.split(" ")
        count = int(count)
        
        if direct == "E":
            origin_fix = x
            y = get_loc(park_list, y, 'y', count, max_y)
        elif direct == "W":
            origin_fix = x
            y = get_loc(park_list, y, 'y', count, max_y, True)
        elif direct == "S":
            origin_fix = y
            x = get_loc(park_list, x, 'x', count, max_x)
        elif direct == "N":
            origin_fix = y
            x = get_loc(park_list, x, 'x', count, max_x, True)
            
    return [x, y]