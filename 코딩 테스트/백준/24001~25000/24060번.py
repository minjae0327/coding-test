n ,loc = map(int, input().split())
nums = list(map(int, input().split()))
count = 0
result = False
answer = 0

def merge(arr, left, mid, right):
    global count
    global result
    global answer
    
    temp = []
    i = left       # left subarray 시작
    j = mid + 1    # right subarray 시작

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
            
    while i <= mid:
        temp.append(arr[i])
        i += 1
    while j <= right:
        temp.append(arr[j])
        j += 1

    for idx in range(len(temp)):
        arr[left + idx] = temp[idx]
        count += 1
        if loc == count:
            answer = temp[idx]
            result = True


def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

merge_sort(nums, 0, n-1)

if result:
    print(answer)
else:
    print(-1)