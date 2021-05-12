from src.app.models.position import Position


class Racket:

    def __init__(self, position: Position, size: int):
        self.position = position
        self.speed = 1
        self.size = size - 1
        self.point = 0

    def move_up(self):
        self.position.y = self.position.y - self.speed

    def move_down(self):
        self.position.y = self.position.y + self.speed
