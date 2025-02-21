dict = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def solution(s):
    answer = ""
    num_key = ""
    
    for i in range(len(s)):
        if "0" <= s[i] <= "9":
                answer += s[i]
        else:
            num_key += s[i]
            if num_key in dict:
                answer += str(dict[num_key])
                num_key = ""
            
    answer = int(answer)
    
    return answer