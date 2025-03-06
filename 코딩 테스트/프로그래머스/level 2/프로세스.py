def solution(priorities, location):
    process_queue = []
    cnt = 0

    for i in range(len(priorities)):
        process_queue.append([i, priorities[i]])
    
    max_priority = max(priorities)
    priorities.remove(max_priority)

    while len(process_queue) != 0:
        process = process_queue.pop(0)
        if process[1] == max_priority:
            cnt += 1
            if process[0] == location:
                # return processes[cnt]
                return cnt 
            max_priority = max(priorities)
            priorities.remove(max_priority)
                
        else:
            process_queue.append(process)