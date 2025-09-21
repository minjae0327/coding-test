a = input().strip()
target = input().strip()
stack = []
len_target = len(target)

for char in a:
    stack.append(char)
    
    
    if len(stack) >= len_target:
        compare = stack[-len_target:]
        if compare == target:
            for _ in range(len_target):
                stack.pop()
                
                
if len(stack) == 0:
    print("FRULA")
else:
    print(stack)