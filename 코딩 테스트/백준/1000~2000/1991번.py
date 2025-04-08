import sys
from collections import defaultdict

input = sys.stdin.readline

n = int(input())
tree = [input().split() for _ in range(n)]

dict_tree = defaultdict(list)
for parent, left, right in tree:
    dict_tree[parent] = [left, right]

def preorder(root):
    if root != '.':
        print(root, end='')          
        preorder(dict_tree[root][0])  
        preorder(dict_tree[root][1]) 

def inorder(root):
    if root != '.':
        inorder(dict_tree[root][0])
        print(root, end='')         
        inorder(dict_tree[root][1]) 

def postorder(root):
    if root != '.':
        postorder(dict_tree[root][0])
        postorder(dict_tree[root][1])
        print(root, end='')  

preorder('A')
print()
inorder('A')
print()
postorder('A')
