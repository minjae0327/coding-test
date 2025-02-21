def get_max_size(column, row, park):
    rect_len = 0
    
    if column - row > 0:
        rect_len = row
    else:
        rect_len = column
    
    max_size = 0
    park = [row[0:rect_len] for row in park[0:rect_len]]
    
    for i in range(rect_len):
        if park[i][i] == "-1":
            _park = [row[0:i] for row in park[0:i]]
            result = all(element == "-1" for row in _park for element in row)
            if result:
                max_size += 1
     
    if result == True:
        return max_size
    else: 
        return -1


def solution(mats, park):
    max_size = 0

    column = len(park)
    row = len(park[0])

    for i in range(column):
        for j in range(row):
            if park[i][j] == "-1":
                _max_size = 1
                
                board = [row_slice[j:row] for row_slice in park[i:column]]

                __max_size = get_max_size(column-i, row-j, board)
                if __max_size > max_size:
                    max_size = __max_size
                        
    if _max_size > max_size:
        max_size = _max_size
    
    mats = sorted(mats)
    mats.reverse()
               
    for mat in mats:
        if mat > max_size:
            continue
        else:
            return mat
        
    return -1