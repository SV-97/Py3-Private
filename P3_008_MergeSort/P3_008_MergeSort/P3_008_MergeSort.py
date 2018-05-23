lst = [4,5,7,1,3,8,6,4,10,2,-20,10.5]
sorted = []

"""
lst = [          1,  2,           3,  4             ]
lst = [     [    1,  2      ],[   3,  4     ]       ]
lst = [     [   [1],[2]     ],[  [3],[4]    ]       ]
"""

def mergesort(lst):
    if (len(lst) <= 1):
        return lst
    else:
        left = lst[:len(lst)//2]
        right = lst[len(lst)//2:]
        left = mergesort(left)
        right = mergesort(right)
        return merge(left, right)

def merge(left, right):
    newlist = []
    while (left != [] and right != []):
        if(left[0] <= right[0]):
            newlist.append(left.pop(0))
        else:
            newlist.append(right.pop(0))
    while (left != []):
        newlist.append(left.pop(0))
    while (right != []):
        newlist.append(right.pop(0))
    return newlist


sorted = mergesort(lst)
print(lst)
print(sorted)