from src.app.services.game import Game
from src.app.models.ball import Ball
from src.app.models.racket import Racket
from src.app.models.table import Table
from src.app.models.position import Position
from blessings import Terminal
import time
from src.rl.third_builder_model.builder_model import build_model


class GameController:

    def __init__(self, size_table: int, size_players: int, game_speed: float,
                 points_win: int = 5, p1_file_model: str = None, p2_file_model: str = None):
        self.game = GameController.build_game(size_table, size_players, points_win, p1_file_model, p2_file_model)
        self.game_speed = game_speed
        self.game.play = True

    @staticmethod
    def build_game(size_table: int, size_players: int,
                   points_win: int, p1_ai: str = None, p2_ai: str = None) -> Game:
        ball = Ball(Position(4, 4))
        table = Table(Position(size_table, 10))
        player1 = Racket(Position(0, 0), size_players)
        player2 = Racket(Position(table.max_position.x, 0), size_players)
        return Game(ball, player1, player2, table, points_win, model1=build_model(p1_ai), model2=build_model(p2_ai))

    def start_game_simple_loop(self):
        term = Terminal()
        while self.game.play:
            with term.location():
                self.game.play_game()
                print(term.move(0, 0) + self.game.render(), end='\r')
                time.sleep(self.game_speed)
