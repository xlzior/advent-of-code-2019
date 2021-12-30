import collections
import math
import queue
import sys
from itertools import combinations

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def angle(self):
        if self.x == 0:                          # edge cases: straight up and straight down
            return 0 if self.y < 0 else math.pi
        raw_angle = math.atan(-self.y / self.x)  # -self.y in order to account for y increasing downwards
        correction = math.pi / 2 if self.x > 0 else 3 * math.pi / 2  # convert tangent info into 360 degrees rotation
        return correction - raw_angle

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) +
                         math.pow(self.y - other.y, 2))

class Asteroid:
    def __init__(self, location):
        self.location = location
        self.distance = base.euclidean(self.location)
        self.angle = math.degrees((self.location - base).angle())

    def __lt__(self, other):
        return self.distance - other.distance < 0


def find_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def find_simplest_delta(point1, point2):
    delta = point2 - point1
    gcd = abs(find_gcd(delta.x, delta.y))
    return Point(delta.x // gcd, delta.y // gcd)

def is_within_line_of_sight(point1, point2):
    delta = find_simplest_delta(point1, point2)
    in_between = point1 + delta
    while in_between != point2:
        if in_between in asteroid_points:
            return False
        in_between += delta
    return True


puzzle_input = open(sys.argv[1]).read().strip().split("\n")
height = len(puzzle_input)
width = len(puzzle_input[0])

asteroid_points = set(Point(x, y) for x in range(width) for y in range(height) if puzzle_input[y][x] == "#")
asteroids_seen = collections.Counter()

# compare all pairs of asteroids and check if they can be seen
for asteroid1, asteroid2 in combinations(asteroid_points, 2):
    if is_within_line_of_sight(asteroid1, asteroid2):
        asteroids_seen[asteroid1] += 1
        asteroids_seen[asteroid2] += 1

base, count = asteroids_seen.most_common(1)[0]
print(f"Part 1: Best is {base} with {count} other asteroids detected")

# sort asteroids into buckets based on angle
asteroids_by_angle = collections.defaultdict(queue.PriorityQueue)
asteroids = set(Asteroid(point) for point in asteroid_points if point != base)
for asteroid in asteroids:
    asteroids_by_angle[asteroid.angle].put(asteroid)

angles = sorted(asteroids_by_angle.keys())
count = 1
angle_index = 0
n = 200
while count <= n:
    angle = angles[angle_index]
    angle_index = (angle_index + 1) % len(angles)
    if asteroids_by_angle[angle].empty():
        continue
    vapourised = asteroids_by_angle[angle].get().location
    if count == n:
        answer = 100 * vapourised.x + vapourised.y
        print(f"Part 2: The {count}th asteroid to be vaporized is at {vapourised}. The answer is {answer}.")
    count += 1
