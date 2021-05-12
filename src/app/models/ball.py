from src.app.models.position import Position


class Ball:

    def __init__(self, position: Position):
        self.position = position
        self.speed = 1
        self.direction = [1, 1]

    def move_y(self):
        self.position.y = self.position.y + self.speed * self.direction[1]

    def move_x(self):
        self.position.x = self.position.x + self.speed * self.direction[0]
