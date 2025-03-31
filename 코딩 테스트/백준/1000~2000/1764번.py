#backjoon
import sys

N, M = map(int, input().split(" "))

n_set = set()
m_set = set()

for _ in range(N):
    n_set.add(sys.stdin.readline().strip())
for _ in range(M):
    m_set.add(sys.stdin.readline().strip())
    
result = sorted(n_set & m_set)

print(len(result))
for name in result:
    print(name)