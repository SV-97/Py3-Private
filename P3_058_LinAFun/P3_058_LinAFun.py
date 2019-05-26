from random import randint


def weighted_value():
    """Values from -16 to 16 weighted around 0"""
    weights = [abs(round(100 - 99*x**2/256 )) for x in range(-16, 17)]
    if randint(0, 1) == 1:
        weights.reverse()
    while True:
        for index, weight in enumerate(weights):
            if randint(0, 120 - weight) == 0:
                return index - 16


m1 = [randint(1, randint(1, 32)) for i in range(randint(1, randint(1, 16)))]

print("sequence =", m1)
print("seq length =", len(m1))

a1 = m1[:]
mutated_a1 = a1[:]

while True:
    for i, element in enumerate(a1):
        if 1 == randint(1, 50): # 2% chance to add weighted value
            mutated_a1[i] = element + weighted_value()
            continue
        if 1 == randint(1, 100): # 1% chance to discard value
            mutated_a1.remove(element)
        if 1 == randint(1, 100): # 1% chance to insert new value 
            mutated_a1.insert(randint(0, len(mutated_a1) - 1), weighted_value())
    if a1 != mutated_a1:
        break

print("a1 =", mutated_a1)