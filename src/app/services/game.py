from src.app.models.ball import Ball
from src.app.models.racket import Racket
from src.app.models.table import Table
from sklearn.neural_network import MLPRegressor
import random
from src.rl.third_builder_model.builder_model import predict


class Game:

    def __init__(self, ball: Ball, player1: Racket, player2: Racket, table: Table,
                 points_win: int, model1: MLPRegressor = None, model2: MLPRegressor = None):
        self.ball = ball
        self.player1 = player1
        self.player2 = player2
        self.ball_init = ball
        self.player1_init = player1
        self.player2_init = player2
        self.table = table
        self.points_win = points_win
        self.model1 = model1
        self.model2 = model2
        self.play = False

    def reset(self):
        self.player1 = self.player1_init
        self.player2 = self.player2_init
        self.ball = self.ball_init
        self.play = False

    def render(self) -> str:
        frame = '\n'
        frame = frame + str(self.player1.point) + " - " + str(self.player2.point)
        frame = frame + '\n'
        for i in range(0, self.table.max_position.y + 1):
            for j in range(0, self.table.max_position.x + 1):
                if self.ball.position.y == i and self.ball.position.x == j:
                    frame = frame + ' O '
                elif self.player1.position.x == j and self.player1.position.y <= i <= (
                        self.player1.position.y + self.player2.size):
                    frame = frame + ' X '
                elif self.player2.position.x == j and self.player2.position.y <= i <= (
                        self.player2.position.y + self.player2.size):
                    frame = frame + ' X '
                elif i == 0 or i == self.table.max_position.y:
                    frame = frame + '---'
                else:
                    frame = frame + '   '
            frame = frame + '\n'
        # print(frame)
        return frame

    def collision_ball_player(self, player: Racket):
        if self.ball.position.x == player.position.x and player.position.y <= self.ball.position.y <= (
                        player.position.y + player.size):
            return True
        return False

    def collision_ball_x(self, x: int):
        if self.ball.position.x == x:
            return True
        return False

    def collision_ball_y(self, y: int):
        if self.ball.position.y == y:
            return True
        return False

    def move_ball(self):
        self.ball.move_y()
        self.ball.move_x()

    def verify_ball_direction(self):
        if self.collision_ball_player(self.player1) or self.collision_ball_x(0) or \
                self.collision_ball_player(self.player2) or self.collision_ball_x(self.table.max_position.x):
            self.ball.direction = [self.ball.direction[0] * -1, self.ball.direction[1]]
        if self.collision_ball_y(0) or self.collision_ball_y(self.table.max_position.y):
            self.ball.direction = [self.ball.direction[0], self.ball.direction[1] * -1]

    def verify_goal(self):
        if self.collision_ball_x(0) and not self.collision_ball_player(self.player1):
            self.player2.point = self.player2.point + 1

        if self.collision_ball_x(self.table.max_position.x) and not self.collision_ball_player(self.player2):
            self.player1.point = self.player1.point + 1

    @staticmethod
    def move_player_random(player: Racket):
        direction = [1, -1]
        value = random.choice(direction)
        if value > 0:
            player.move_down()
        else:
            player.move_up()

    def verify_player_offset(self, player: Racket):
        if player.position.y < 0:
            player.move_down()
        elif player.position.y + player.size > self.table.max_position.y:
            player.move_up()

    def move_player_1(self):
        if self.model1 is None:
            Game.move_player_random(self.player1)
        else:
            if(predict(self.model1, self.player1.position.x, self.player1.position.y,
                       self.ball.position.x, self.ball.position.y) == "UP"):
                self.player1.move_up()
            else:
                self.player1.move_down()

    def move_player_2(self):
        if self.model2 is None:
            Game.move_player_random(self.player2)
        else:
            if (predict(self.model2, self.player2.position.x, self.player2.position.y,
                        self.ball.position.x, self.ball.position.y) == "UP"):
                self.player2.move_up()
            else:
                self.player2.move_down()

    def verify_winner(self):
        if self.player1.point == self.points_win:
            self.reset()
            print("\t\t\t\tWINNER PLAYER 1")

        if self.player2.point == self.points_win:
            print("\t\t\t\tWINNER PLAYER 2")
            self.reset()

    def play_game(self):
        self.move_player_1()
        self.move_player_2()
        self.verify_player_offset(self.player1)
        self.verify_player_offset(self.player2)
        self.move_ball()
        self.verify_ball_direction()
        self.verify_goal()
        self.verify_winner()
