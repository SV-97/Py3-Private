import cv2
import matplotlib.pyplot as plt
import numpy as np

dimension = (650, 650)


class Point():
    def __init__(self, x, y, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color

    def distance_to(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __str__(self):
        return f"({self.x}|{self.y})"

    def __hash__(self):
        return hash((round(self.x, 8), round(self.y, 8)))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Vector(complex):
    def __new__(cls, a, b):
        """Construct vector from point a to b"""
        return super().__new__(cls, b.x - a.x, b.y - a.y)


class Line():
    def __init__(self, vector, point):
        slope = 1j * vector
        self.m = slope.imag / slope.real
        self.x_p = point.x + vector.real
        self.y_p = point.y + vector.imag
    
    def intersect(self, other):
        if self.m == other.m:
            return None
        x = (self.m*self.x_p - other.m*other.x_p - self.y_p + other.y_p) / (self.m - other.m)
        return Point(x, self.m*(x - self.x_p) + self.y_p)

points = [
    Point(200, 200, (64, 0, 0)),
    Point(600, 600, (0, 64, 0)),
    Point(100, 300, (0, 0, 64)),
    Point(400, 100, (64, 64, 0))
]

grid = [[Point(x, y) for x in range(dimension[0])] for y in range(dimension[1])]

for row in grid:
    for point in row:
        distances = [point.distance_to(source_point) for source_point in points]
        min_ = min(distances)
        closest_point = next(filter(lambda source_point: True if point.distance_to(source_point) == min_ else False, points))
        point.color = closest_point.color

image = [[point.color if point not in points else (255, 255, 255) for point in row ] for row in grid]

plt.subplot(1, 2, 1)
plt.imshow(image)

lines = []
for point in points:
    vectors = [Vector(point, other) * 0.5 for other in points]
    for vector in vectors:
        if vector == 0:
            continue
        lines.append(Line(vector, point))
lines = set(lines)

intersections = [line_1.intersect(line_2) for line_1 in lines for line_2 in lines]
intersections = (point for point in intersections if point is not None )
intersections = set(intersections)
for point in intersections:
    try:
        image[round(point.x)][round(point.y)] = (255, 255, 255)
    except IndexError:
        print(f"{round(point.x)}, {round(point.y)} was out of bounds")

plt.subplot(1, 2, 2)
plt.imshow(image)
plt.show()