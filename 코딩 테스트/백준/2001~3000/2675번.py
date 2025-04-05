N = int(input())

for _ in range(N):
    nums, string = list(input().split())

    new_string = ""
    for i in range(len(string)):
        new_string = new_string + (string[i] * int(nums))
        
    print(new_string)