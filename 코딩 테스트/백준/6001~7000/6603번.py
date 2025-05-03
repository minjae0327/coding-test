def lotto(arr, nums, index, depth):
    if depth == 6:
        print(*arr)
        return

    for i in range(index, len(nums)):
        arr[depth] = nums[i]
        lotto(arr, nums, i + 1, depth + 1)

while True:
    nums = list(map(int, input().split()))
    if nums[0] == 0:
        break
    arr = [0] * 6
    lotto(arr, nums[1:], 0, 0)
    print()