lst = [4,5,7,1,3,8,6,4,10,2,-20,10.5]
sorted = []

while len(lst) > 1:
    min = lst[0]
    for i in range(len(lst)):
        if lst[i] < min:
            min = lst[i]
    sorted.append(lst.pop(lst.index(min)))
sorted.append(lst.pop(0))

print(lst)
print(sorted)