from .transform import *

class BoxCollider:
    def __init__(self, center: Point2D, width, height, enable=True):
        self.enable = enable
        self.top_left_point = Point2D(center.x - width / 2, center.y - height / 2)
        self.bottom_right_point = Point2D(center.x + width / 2, center.y + height / 2)

    # loop all element size by cell in this box
    def map(self, cell_size, func):
        min = self.pos2cell(self.top_left_point, cell_size)
        max = self.pos2cell(self.bottom_right_point, cell_size)

        for i in range(min.x, max.x + 1):
            for j in range(min.y, max.y + 1):
                func(i, j)

    def calculate_cell(self, cell_size, obj, content: dict):
        if not self.enable:
            return
        def append_value(i, j):
            if content.keys().__contains__((i, j)):
                content.get((i, j)).append(obj)
            else:
                content.setdefault((i, j), []).append(obj)

        self.map(cell_size, append_value)

    def pos2cell(self, pos: Point2D, cell_size):
        return Point2D(int(pos.x / cell_size), int(pos.y / cell_size))


class CircleCollier:
    def __init__(self, center: Point2D, radius, enable=True):
        self.enable = enable
        self.center = center
        self.radius = radius

    # loop all element size by cell in this box
    def map(self, cell_size, func):
        top_left_point = Point2D(self.center.x - self.radius, self.center.y - self.radius)
        bottom_right_point = Point2D(self.center.x + self.radius, self.center.y + self.radius)

        min = self.pos2cell(top_left_point, cell_size)
        max = self.pos2cell(bottom_right_point, cell_size)
        center = Point2D((min.x + max.x) / 2, (min.y + max.y) / 2)
        r = int(self.radius / cell_size)

        for i in range(min.x, max.x + 1):
            for j in range(min.y, max.y + 1):
                if (i - center.x) ** 2 + (j - center.y) ** 2 > r ** 2:
                    continue
                func(i, j)

    def calculate_cell(self, cell_size, obj, content: dict):
        if not self.enable:
            return

        def append_value(i, j):
            if content.keys().__contains__((i, j)):
                content.get((i, j)).append(obj)
            else:
                content.setdefault((i, j), []).append(obj)

        self.map(cell_size, append_value)

    def pos2cell(self, pos: Point2D, cell_size):
        return Point2D(int(pos.x / cell_size), int(pos.y / cell_size))


class SpatialHashmap:
    def __init__(self, width, height, cell_size):
        self.objs = []
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.content = dict()

    def append_obj(self, obj):
        self.objs.append(obj)
    
    def pop_obj(self):
        if len(self.objs) > 0:
            self.objs.pop()
            return 1
        return 0

    def calculate_collision(self):
        for obj in self.objs:
            obj.collider.calculate_cell(self.cell_size, obj, self.content)

    def call_collision(self, obj_index):
        if obj_index >= len(self.objs):
            return None
        obj_colliders = []

        def check_value(i, j):
            if self.content.get((i, j)) and len(self.content.get((i, j))) > 1:
                for obj in self.content.get((i, j)):
                    if obj != self.objs[obj_index] and obj not in obj_colliders:
                        obj_colliders.append(obj)

        self.objs[obj_index].collider.map(self.cell_size, check_value)

        result = 0
        for obj in obj_colliders:
            print("%s -> %s" % (self.objs[obj_index].obj_type, obj.obj_type))
            result = self.objs[obj_index].on_collision(obj)
        return result


    def clear_data(self):
        self.content.clear()

    def call_collision_all(self):
        for i in range(len(self.objs)):
            self.call_collision(i)