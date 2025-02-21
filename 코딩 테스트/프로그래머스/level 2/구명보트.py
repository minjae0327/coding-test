def solution(people, limit):
    answer = 0
    
    people = sorted(people)
    
    light = 0
    heavy = len(people) - 1
    
    while light <= heavy:
        if people[heavy] + people[light] <= limit:
            light += 1
            
        heavy -= 1
        
        answer += 1
        
    
    return answer