

class Vector2D:
    x=None
    y=None
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, target):
        self.x += target.x
        self.y += target.y

    def subtract(self, target):
        self.x -= target.x
        self.y -= target.y

    def multiply(self, target):
        self.x *= target.x
        self.y *= target.y

    def divide(self, target):
        self.x /= target.x
        self.y /= target.y