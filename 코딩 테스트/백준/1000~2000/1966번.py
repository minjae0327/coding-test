# backjoon
case = int(input())

answer = []

for _ in range(case):
    N, target = map(int, input().split(" "))
    
    dict = {}
    arr = list(map(int, input().split()))

    for i in range(N):
        dict[i+1] = arr[i]
        
    max_key = max(dict, key=dict.get)

    first_key = list(dict.keys())[0]
    loc = 1

    while True:
        first_key = list(dict.keys())[0]
        
        if (first_key == target + 1) and first_key == max_key:
            answer.append(loc)
            break
        
        if first_key != max_key:
            a = dict[first_key]
            del dict[first_key]
            dict[first_key] = a
        else:
            loc += 1
            del dict[first_key]
            max_key = max(dict, key=dict.get)

    
for i in answer:
    print(i)