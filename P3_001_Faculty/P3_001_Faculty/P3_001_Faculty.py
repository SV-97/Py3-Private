while True:
    input1 = int(input("Input a natural number: "))
    if input1 < 0 :
        print("Negative numbers aren't allowed")
        continue
    output = 1
    for i in range(2, input1 + 1 ):
        output = output * i
    print("The faculty of " , input1 , " is " , output)
