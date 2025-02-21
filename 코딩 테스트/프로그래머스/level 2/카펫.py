def solution(brown, yellow):
    total = brown + yellow  # 전체 격자의 수
    for width in range(3, int(total ** 0.5) + 1):  # 가로 길이를 3부터 시작하여 전체 격자의 제곱근까지 확인
        if total % width == 0:  # 가로 길이가 전체 격자의 약수인 경우
            height = total // width  # 세로 길이 계산
            if (width - 2) * (height - 2) == yellow:  # 노란색 격자의 수가 맞는지 확인
                return [max(width, height), min(width, height)]  # 가로가 세로보다 크거나 같도록 반환
    return []

print(solution(10, 2))
print(solution(8, 1))
print(solution(24, 24))
print(solution(14, 4))