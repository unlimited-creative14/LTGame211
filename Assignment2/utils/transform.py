class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Transform:
    def __init__(self, position: Point2D, rotation=0):
        self.position = position
        self.rotation = rotation

    def translate(self, x, y):
        self.position.x += x
        self.position.y += y