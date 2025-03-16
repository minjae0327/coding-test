def solution(progresses, speeds):
    answer = []
    pin = 0
    length = len(progresses)

    while pin != length:
        count = 0
        for i in range(length):
            progresses[i] += speeds[i]
        while progresses[pin] >= 100:
            count += 1
            pin += 1
            if pin == length:
                break
        
        if count != 0:
            answer.append(count)
            
    return answer