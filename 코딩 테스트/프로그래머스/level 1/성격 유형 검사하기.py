def solution(survey, choices):
    character_dict = {
    "T" : 0,
    "R" : 0,
    "F" : 0, 
    "C" : 0,
    "M" : 0,
    "J" : 0,
    "N" : 0,
    "A" : 0
    }

    for i in range(len(survey)):
        if choices[i] > 4:
            character_dict[survey[i][1]] += choices[i] - 4
        elif choices[i] < 4:
            character_dict[survey[i][0]] += 4 - choices[i]
        else:
            continue

    character_list = list(character_dict.items())

    answer = ""

    for i in range(0, 8, 2):
        if character_list[i][1] > character_list[i+1][1]:
            answer += character_list[i][0]
        elif character_list[i][1] < character_list[i+1][1]:
            answer += character_list[i+1][0]
        else:
            answer += character_list[i][0] if character_list[i][0] < character_list[i+1][0] else character_list[i+1][0]
            
            
    return answer