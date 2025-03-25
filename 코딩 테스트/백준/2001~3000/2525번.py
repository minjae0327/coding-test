hour, minute = map(int, input().split(" "))
_min = int(input())

minute += _min

if minute >= 60:
    hour += minute // 60
    minute = minute % 60
if hour >= 24:
    hour = hour % 24
    
print(hour, minute)
