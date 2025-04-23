n = int(input())

words = [input().strip() for _ in range(n)]

def recursion(word, l, r, count):
    count += 1
    if l >= r:
        return 1, count
    elif word[l] != word[r]:
        return 0, count
    else:
        return recursion(word, l + 1, r - 1, count)

def isPalindrome(word):
    return recursion(word, 0, len(word) - 1, 0)

for word in words:
    result, count = isPalindrome(word)
    print(result, count)
