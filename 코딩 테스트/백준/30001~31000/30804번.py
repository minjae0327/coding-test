import sys
from collections import defaultdict

input = sys.stdin.readline

n = int(input())
num = list(map(int, input().split()))

count_dict = defaultdict(int)
a, b = 0, 0
result = 0

while b < n:
    #과일 갯수 증가
    count_dict[num[b]] += 1
    
    #과일 종류가 2개 이상이면
    while len(count_dict) > 2:
        #맨 앞에거 하나 뺴기
        count_dict[num[a]] -= 1
        #그 과일 종류가 아에 없으면 dict에서 종류 제거
        if count_dict[num[a]] == 0:
            del count_dict[num[a]]
        #a위치 증가
        a += 1
    
    result = max(result, b - a + 1)
    b += 1

print(result)
