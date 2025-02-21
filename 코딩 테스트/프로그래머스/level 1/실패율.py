def solution(N, stages):
    answer = []
    
    length = len(stages)
    sorted_stages = sorted(stages)
    
    stage_dict = {}
    
    for n in range(N):
        stage_dict[n+1] = 0
        
    for i in range(length):
        if not stages[i] > N:
            stage_dict[stages[i]] += 1
    
    fail_stages = {}
         
    for n in range(N):
        if stage_dict[n+1] == 0:
            fail_stages[n+1] = 0
        else:
            fail_stages[n+1] = stage_dict[n+1]/length
        
        length -= stage_dict[n+1]
        
    sorted_stages = dict(sorted(fail_stages.items(), key=lambda x : x[1], reverse=True))
    answer = list(sorted_stages.keys())
    
    return answer