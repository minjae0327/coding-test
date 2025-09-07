from collections import Counter

n = int(input())

sales_list = []

for i in range(n):
    sales_list.append(input().strip())
    
sales_count = Counter(sales_list)
most_saled = sales_count.most_common()
most_saled.sort(key=lambda x: (-x[1], x[0]))

print(most_saled[0][0])