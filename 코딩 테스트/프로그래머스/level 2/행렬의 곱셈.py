def solution(array1, array2):
    if len(array1[0]) == len(array2):
        arr1 = array1
        arr2 = array2
    else:
        arr1 = array2
        arr2 = array1
    
    row = len(arr1)
    column = len(arr1[0])

    answer = []

    for i in range(row):
        arr = arr1[i]
        results = []
        for j in range(len(arr2[0])):
            result = 0
            for k in range(len(arr2)):
                result += arr[k] * arr2[k][j]
                
            results.append(result)
            
        answer.append(results)
    
    return answer