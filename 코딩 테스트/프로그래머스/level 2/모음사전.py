def solution(word):
    dict = {
        "A" : 0,
        "E" : 1,
        "I" : 2,
        "O" : 3,
        "U" : 4,
    }
    weights = [781, 156, 31, 6, 1]

    answer = 0

    for i, char in enumerate(word):
        answer += dict[char] * weights[i]

    return (answer + len(word))