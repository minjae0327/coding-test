# 순열 사용
import itertools

def solution(k, dungeons):
    npr = list(itertools.permutations(dungeons, len(dungeons)))

    answer = 0

    for i in range(len(npr)):
        _npr = npr[i]
        curr_k = k
        count = 0
        
        for j in range(len(_npr)):
            if curr_k >= _npr[j][0]:
                curr_k -= _npr[j][1]
                count += 1
                
        if count > answer:
            answer = count
            
    return answer


#dfs 사용
