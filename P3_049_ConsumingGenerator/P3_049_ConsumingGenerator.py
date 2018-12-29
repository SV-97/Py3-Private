def summator():
    sum_ = 0
    while True:
        sum_ += (yield)
        print(sum_)

summator = summator()
next(summator)

summator.send(5)
summator.send(10)
summator.send(2)
