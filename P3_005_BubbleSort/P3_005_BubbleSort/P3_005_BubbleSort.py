lst = [4,5,7,1,3,8,6,4,10,2,-20,10.5]
sorted = []

while len(lst) > 1:
    for i in range(len(lst)-1,0,-1): #go through array in reverse
        r = lst[i]
        l = lst[i-1]
        if r < l:
            lst[i] = l
            lst[i-1] = r
        if i == 1:
            sorted.append(lst.pop(0))
sorted.append(lst.pop(0))

print(lst)
print(sorted)