class Squares():
    """Iterate over all squares in given range
    """
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def __iter__(self):
        i = self.start
        while i < self.end:
            yield (i, i**2)
            i += 1

class SquaresWithoutGenerator():
    """Iterate over all squares in given range
    """
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def __iter__(self):
        self.i = self.start
        return self
    def __next__(self):
        if self.i < self.end:
            self.i += 1
            return (self.i-1, (self.i-1)**2)
        else:
            raise StopIteration

a = []
b = []
print("---------WITH GENERATOR---------")
for base, square in Squares(10,20):
    print("{}² = {}".format(base, square))
    for base2, square2 in Squares(base*2, base*2+1):
        print("{}² = {}".format(base2, square2))
    a.append(square)
    a.append(square2)

print("---------WITHOUT GENERATOR---------")
for base, square in SquaresWithoutGenerator(10,20):
    print("{}² = {}".format(base, square))
    for base2, square2 in SquaresWithoutGenerator(base*2, base*2+1):
        print("{}² = {}".format(base2, square2))
    b.append(square)
    b.append(square2)

if a == b:
    print("Squares == SquaresWithoutGenerator")