def solution(citations):
    citations = sorted(citations)
    max_len = 0

    for citation in citations:
        length = len([x for x in citations if x >= citation])
        
        temp = min(length, citation)
        if max_len < temp:
            max_len = temp
        
    return max_len

print(solution([3,3,3,4]))