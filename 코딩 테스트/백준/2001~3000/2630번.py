# backjoon
def is_all_ones(matrix):
    for row in matrix:
        for element in row:
            if element != 1:
                return False
    return True

def is_all_zeros(matrix):
    for row in matrix:
        for element in row:
            if element != 0:
                return False
    return True

def check_square(matrix, size, white, blue):
    if is_all_zeros(matrix):
        white += 1
    elif is_all_ones(matrix):
        blue += 1
    else:
        half = size // 2
        top_left     = [row[:half] for row in matrix[:half]]
        top_right    = [row[half:] for row in matrix[:half]]
        bottom_left  = [row[:half] for row in matrix[half:]]
        bottom_right = [row[half:] for row in matrix[half:]]

        white, blue = check_square(top_left, half, white, blue)
        white, blue = check_square(top_right, half, white, blue)
        white, blue = check_square(bottom_left, half, white, blue)
        white, blue = check_square(bottom_right, half, white, blue)

    return white, blue


import sys
input = sys.stdin.readline

N = int(input())

matrix = []
white, blue = 0, 0


for _ in range(N):
    matrix.append(list(map(int, input().split())))
    
white, blue = check_square(matrix, N, white, blue)  

print(white)
print(blue)