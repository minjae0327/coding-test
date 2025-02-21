def solution(n):
    answer = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            if i % 2 == 1:
                answer += 1
            if i != n // i and (n // i) % 2 == 1:
                answer += 1
                
    return answer

print(solution(15))
print(solution(1001))