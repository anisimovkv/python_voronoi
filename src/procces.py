from heapq import heappop, heappush
from typing import List
from enum import Enum

X: int = 0
Y: int = 1


class Point:
    def __init__(self, p, idx=None):
        self.x = round(p[X], 4)
        self.y = round(p[Y], 4)


class Site:
    def __init__(self, site: Point):
        self.site: Point = site


class Event:
    def __init__(self, pt: Point, site: Site):
        self.pt: Point = pt
        self.site: Site = site


class Voronoi:
    """bla blba"""

    def __init__(self):
        self.points = []
        self.stillOnFirstRow = True
        self.first_point = None
        self.tree = None
        self.edge = []
        self.pq = []

    def process(self, points: List):
        for idx in range(len(points)):
            pt: Point = Point(points[idx], idx)
            self.points.append(pt)
            event: Event = Event(pt, site=pt)
            heappush(self.pq, event)

        while self.pq:
            event = heappop(self.pq)
            if event.deleted:
                continue

        self.sweep_point = event.p

        if event.site:
            self.process_site(event)
        else:
            self.process_circle(event)

        # edge without point, ray
        if self.tree and not self.tree.is_leaf:
            self.finish_edges(self.tree)
            # end edge of voronoi
            for e in self.edges:
                if e.partner:
                    if e.b is None:
                        e.start.y = self.height
                    else:
                        e.start = e.partner.end

    def process_site(self, event: Event):
        if self.tree is None:
            self.tree = Arc(event.p)
            self.first_point = event.p
            return

        # Должна обрабатывать особый случай, когда две точки имеют
        # одну и ту же наивысшую кординату y. В таком случае корень
        # представляет собой лист. Обратите внимание, что при сортировке
        # событий эти точки упорядочиваются по коордитнате x, так что
        # следующая точка находится справа.
        if self.tree.is_leaf and event.y == self.tree.site.y:
            left = self.tree
            right = Arc(event.p)
            start = Point(((self.first_point.x+self.event.p.x)/2,self.height))
            edge = VoronoiEdge(start, self.first_point, event.p)
            self.tree = Arc(edge = edge)
            self.tree.set_left(left)
            self.tree.set_right(right)
            self.edges.append(edge)

    def proccess_circle(self, event: Event):
        pass


class Arc:
    def __init__(self, point: Point):
        self.p = point
