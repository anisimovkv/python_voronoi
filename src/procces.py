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
            start = Point(
                ((self.first_point.x + self.event.p.x) / 2, self.height))
            edge = VoronoiEdge(start, self.first_point, event.p)
            self.tree = Arc(edge=edge)
            self.tree.set_left(left)
            self.tree.set_right(right)
            self.edges.append(edge)
            return
        # Если лист представляет собой событие окружности, он больше
        # не является корректным, поскольку разделяется
        leaf = self.find_arc(event.p.x)
        if leaf.circle_event:
            leaf.circle_event.deleted = True
        # Находим точку параболы, где event.pt.x разбивает ее пополам
        # вертикальной линией
        start = leaf.point_on_bisection_line(event.p.x, self.sweep_pt.y)

        # Между двумя узлами находятся потенциальные ребра Вороного
        neg_ray = VoronoiEdge(start, leaf.site, event.p)
        pos_ray = VoronoiEdge(start, event.p, leaf.site)
        self.edge.append(neg_ray)

        # Изменение побережья новыми внутренними узалами
        leaf.edge = pos_ray
        leaf.is_leaf = False

        left = Arc()
        leaf.edge = neg_ray
        leaf.set_left(Arc(leaf.site))
        leaf.set_right(Arc(leaf.site))

        # Проверка наличия потениального событие
        # окружности слева или справа.
        self.generate_circle_event(leaf.left)
        self.generate_circle_event(leaf.right)

    def proccess_circle(self, event: Event):
        node = event.node

        left_a = node.get_left_ancestor()
        left = left_a.get_largest_descendant()
        right_a = node.get_right_ancestor()
        right = right_a.get_smallest_decendant()

        if left.circle_event:
            left.circle_event.deleted = True
        if right.circle_event:
            right.circle_event.deleted = True

        p = node.point_on_bisection_line(event.p.x, self.sweep_point.y)
        left_a.edge.end = p
        right_a.edge.end = p

        t = node
        ancestor = None
        while t != self.tree:
            t = t.parent
            if t == left_a:
                ancestor = left_a
            elif t == right_a:
                ancestor = right_a
        ancestor.edge = VoronoiEdge(p, left.site, right.site)
        self.edges.append(ancestor.edge)

        node.remove()

        self.generate_circle_event(left)
        self.generate_circle_event(right)


class Arc:
    def __init__(self, point: Point):
        self.p = point
