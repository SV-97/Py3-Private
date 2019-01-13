from time import time

def sub_normalize(a1, a2, index):
    """Vector subtraction of a1 - a2 so that index is 0"""
    factor = a1[index] / a2[index]
    return [a1[i] - factor * a2[i] for i in range(len(a1))]


def get_L(a, index):
    """Get solution matrix where index is your reference index in a"""
    l = [[0 if i != j else 1 for i in range(len(a))] for j in range(len(a[0]))]

    for i in range(len(a) - 1, index, -1):
        factor = a[i][index] / a[index][index]
        l[i][index] = -factor
    return l


def det(a):
    """Determinant of matrix"""
    if len(a) == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    else:
        sum_ = 0
        for row in range(len(a)):
            if (row + 1) % 2:
                sign = 1
            else:
                sign = -1
            sum_ += sign * a[row][0] * det([a[j][1:] for j in range(len(a)) if j != row])
        return sum_


def mat_mult(a1, a2):
    """Matrix multiplication"""
    c = [[0 for i in range(len(a2[0]))] for i in range(len(a1))]
    for i in range(len(c)):
        for j in range(len(a2)):
            for k in range(len(c[0])):
                c[i][k] += a1[i][j] * a2[j][k]
    return c


def invers_frobenius(a):
    """Invers of a Frobenius matrix"""
    for row in range(1, len(a)):
        for column in range(len(a[0])):
            a[row][column] *= -1
    return a


# A*x = b
a = [
    [2, 1, 1, 0], 
    [4, 3, 3, 1], 
    [8, 7, 9, 5],
    [6, 7, 9, 8]
    ]

b = [[1], [2], [3], [4]]
x = ["x1", "x2", "x3", "x4"]

print("A = ", a)

l1 = get_L(a, 0)
print("L1 = ", l1)
a = mat_mult(l1, a)
print("L1*A = ", a)

l2 = get_L(a, 1)
print("L2 = ", l2)
a = mat_mult(l2, a)
print("L2*L1*A = ", a)

l3 = get_L(a, 2)
print("L3 = ", l3)
a = mat_mult(l3, a)
print("L3*L2*L1*A = ", a)

b = mat_mult(l1, b)
print("L1*b = ", b)
b = mat_mult(l2, b)
print("L2*L1*b = ", b)
b = mat_mult(l3, b)
print("L3*L2*L1*b = ", b)

dimension = len(a)

solved_x = []
for row in range(len(x) -1 , -1, -1):
    sum_ = []
    for x in range(len(solved_x) -1, -1, -1):
        sum_.append(a[row][dimension - 1 - x] * solved_x[x])
    solved_x.append((b[row][0] - sum(sum_)) / a[row][dimension - 1 - len(solved_x)])

solved_x = list(reversed(solved_x))

print("x = ", solved_x)


# A*x = b
# shape of a is [rows][columns]
a = [
    [2, 1, 1, 0, 3, 5], 
    [4, 3, 3, 1, 7, 0], 
    [8, 7, 9, 5, 1, 6],
    [6, 7, 9, 8, 9, 1],
    [7, 2, 9, 6, 3, 2],
    [3, 4, 2, 9, 8, 6]
    ]
b = [[1], [2], [3], [4], [5], [6]]
x = ["x1", "x2", "x3", "x4", "x5", "x6"]


def solve_lineq_gauss(matrix, vector):
    a = [matrix[i][:] for i in range(len(matrix))]
    b = [vector[i][:] for i in range(len(vector))]
    for i in range(len(matrix)):
        l_i = get_L(a, i)
        a = mat_mult(l_i, a)
        b = mat_mult(l_i, b)
    
    dimension = len(a)
    solved_x = []
    for row in range(len(vector) -1 , -1, -1):
        already_solved = [a[row][dimension - 1 - x] * solved_x[x] for x in range(len(solved_x) -1, -1, -1)]
        solved_x.append((b[row][0] - sum(already_solved)) / a[row][dimension - 1 - len(solved_x)])
    return list(reversed(solved_x))

solution = None
t1 = time()
solution = solve_lineq_gauss(a, b)
t2 = time()
print(f"Got x = {solution} in {t2-t1:.2e}s")