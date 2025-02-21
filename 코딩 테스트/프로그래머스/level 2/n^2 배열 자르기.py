def solution(s):
    s = s.strip("{}")
    s = s.split("},{")
    tp = tuple(tuple(map(int, subset.split(","))) for subset in s)

    tp_dict = {}

    for i in range(len(tp)):
        for j in range(len(tp[i])):
            tp_dict[tp[i][j]] = 0
            
    for i in range(len(tp)):
        for j in range(len(tp[i])):
            tp_dict[tp[i][j]] += 1
            
    sorted_list = sorted(tp_dict.items(), key=lambda x : x[1], reverse = True)
    answer = [sorted_list[i][0] for i in range(len(sorted_list))]
    
    return answer