def solution(answers):
    answer = []
    
    person1 = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    person2 = [2, 1, 2, 3, 2, 4, 2, 5]
    person3 = [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    
    score1 = 0
    score2 = 0
    score3 = 0
    
    for i in range(len(answers)):
        if answers[i] == person1[i%10]:
            score1 += 1
        if answers[i] == person2[i%8]:
            score2 += 1
        if answers[i] == person3[i%10]:
            score3 += 1    
    
    score = [score1, score2, score3]
    max_score = max(score)
    
    if max_score == score[0]:
        answer.append(1)
    if max_score == score[1]:
        answer.append(2)
    if max_score == score[2]:
        answer.append(3)
         
    
    return answer