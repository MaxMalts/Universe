class Vector2:
    x = 0
    y = 0


    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    

    def __add__(self, other): 
        return Vector2(self.x + other.x, self.y + other.y)
    

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    

    def __mul__(self, num):
        return Vector2(self.x * num, self.y * num)
    

    def __rmul__(self, num):
        return Vector2(self.x * num, self.y * num)
    

    def __truediv__(self, num):
        return Vector2(self.x / num, self.y / num)
    

    def __rtruediv__(self, num):
        return Vector2(self.x / num, self.y / num)


    def __neg__(self):
        return Vector2(-self.x, -self.y)