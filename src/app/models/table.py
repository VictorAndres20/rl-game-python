from src.app.models.position import Position


class Table:

    def __init__(self, max_position: Position):
        self.max_position = max_position
        self.max_position.x = self.max_position.x - 1
        self.max_position.y = self.max_position.y - 1
