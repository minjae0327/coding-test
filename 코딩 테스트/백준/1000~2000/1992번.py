import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

n = int(input())
area = [list(map(int, input().strip())) for _ in range(n)]

result = ""

def is_one_or_zero(area):
    first = area[0][0]
    for row in area:
        for cell in row:
            if cell != first:
                return None
    return first

def quadtree(area, size):
    global result

    answer = is_one_or_zero(area)
    if answer == 1:
        result += "1"
    elif answer == 0:
        result += "0"
    else:
        result += "("
        half = size // 2

        top_left = [row[:half] for row in area[:half]]
        top_right = [row[half:] for row in area[:half]]
        bottom_left = [row[:half] for row in area[half:]]
        bottom_right = [row[half:] for row in area[half:]]

        quadtree(top_left, half)
        quadtree(top_right, half)
        quadtree(bottom_left, half)
        quadtree(bottom_right, half)

        result += ")"

quadtree(area, n)
print(result)
