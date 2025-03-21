from collections import Counter

def solution(k, tangerine):
    count = Counter(tangerine)
    freq = sorted(count.values(), reverse=True)

    total = 0
    type = 0

    for i in freq:
        total += i
        type += 1
        if total >= k:
            return type