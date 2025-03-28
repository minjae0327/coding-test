# backjoon
import sys

def get_cable_num(list, longest):
    length = 0
    
    for i in range(len(list)):
        length += list[i] // longest
        
    return length

def binary_search(cables, target_num):
    left = 1
    right = max(cables)
    result = 0
    
    while left <= right:
        longest = (left + right) // 2
        count = get_cable_num(cables, longest)
        
        if count >= target_num:
            result = longest
            left = longest + 1
        else:
            right = longest - 1

    return result

K, N = map(int, input().split())
cables = [int(input()) for _ in range(K)]
print(binary_search(cables, N))