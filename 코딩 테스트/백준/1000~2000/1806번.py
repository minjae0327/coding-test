n, s = map(int, input().split())
nums = list(map(int, input().split()))

length = float("inf")

left, right = 0, 0
current_sum = 0

while right < n:
    current_sum += nums[right]
    
    while current_sum >= s:
        length = min(length, right - left + 1)
        current_sum -= nums[left]
        left += 1
        
    right += 1
    
if length == float('inf'):
    print(0)
else:
    print(length)