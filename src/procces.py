from heapq import heappop, heappush
from typing import List
from enum import Enum


class Coordinate(Enum):
    X = 0
    Y = 1


class Point:
    def __init__(self, p, idx=None):
        self.x = round(p[X], 4)
        self.y = round(p[Y], 4)


class Voronoi:
    """bla blba"""

    def process(self, points: List):
        self.pq = []
        self.edge = []
        self.tree = None
        self.first_point = None
        self.stillOnFirstRow = True
        self.points = []

        for idx in range(len(points)):
            pt = Point(points[idx], idx)
