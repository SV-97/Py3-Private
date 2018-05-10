lst = [4,5,7,1,3,8,6,4,10,2,-20,10.5]
sorted = []

sorted.append(lst.pop(0))
while len(lst) > 0:
    n = lst.pop(0)
    for i in range(len(sorted)-1,-1,-1):
        if (sorted[i] < n):
            sorted.insert(i+1,n)
            break
        elif len(sorted)> 1 and i == 0:
            sorted.insert(i,n)
            break

print(lst)
print(sorted)