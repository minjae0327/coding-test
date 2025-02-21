def get_coord(wallpaper):
    coord = []
    
    column = len(wallpaper)
    row = len(wallpaper[0])
    
    for i in range(column):
        for j in range(row):
            if wallpaper[i][j] == "#":
                coord.append([i, j])
                
    print(coord)
    return coord
            

def solution(wallpaper):
    coordinates = get_coord(wallpaper)
    if len(coordinates) == 1:
        return [coordinates[0][0], coordinates[0][1], coordinates[0][0]+1, coordinates[0][1]+1]
    
    min_column = coordinates[0][0]
    max_column = coordinates[0][0]
    min_row = coordinates[0][1]
    max_row = coordinates[0][1]
    
    for coordinate in coordinates:
        if coordinate[0] > max_column:
            max_column = coordinate[0]
        if coordinate[0] < min_column:
            min_column = coordinate[0]
            
        if coordinate[1] > max_row:
            max_row = coordinate[1]
        if coordinate[1] < min_row:
            min_row = coordinate[1]
    
    answer = [min_column, min_row, max_column+1, max_row+1]
    
    return answer