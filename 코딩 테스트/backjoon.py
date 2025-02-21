iter = int(input())

chars = []


for i in range(iter):
    chars.append(input())

for i in range(iter):
    test_list = []
    for j in range(len(chars[i])):
        char = chars[i][j]
        test_list.append(char)
        
        if char == ')' and len(test_list) != 0:
            if test_list[-1] == '(':
                test_list.pop()
                test_list.pop()
                
    if len(test_list) == 0:
        print("YES")
    else:
        print("NO")
        