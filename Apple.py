class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isEaten = False

    def Location(self):
        position = {
            'x': self.x,
            'y': self.y
        }
        return position
    
    def checkIsEaten(self):
        return self.isEaten