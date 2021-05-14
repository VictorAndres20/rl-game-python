from src.app.controllers.game_controller import GameController
from src.app.models.ball import Ball
from src.app.models.racket import Racket
import time
from typing import List
from blessings import Terminal


# ENVIRONMENT
table_size = 21
game_speed = 0.1
simulations = 3000
player_size = 3


def build_action(y_cache: List, player: Racket) -> str:
    if y_cache[len(y_cache) - 2] < player.position.y:
        return "DOWN"
    elif y_cache[len(y_cache) - 2] > player.position.y:
        return "UP"
    else:
        return "NONE"


def build_strict_reward(player: Racket, ball: Ball) -> int:
    if player.position.y <= ball.position.y <= (player.position.y + player.size):
        return 1
    elif player.position.y > ball.position.y:
        return abs(ball.position.y - player.position.y) * -1
    elif (player.position.y + player.size) < ball.position.y:
        return abs(ball.position.y - (player.position.y + player.size)) * -1


def build_binary_reward(player: Racket, ball: Ball) -> int:
    if player.position.x == ball.position.x:
        if player.position.y <= ball.position.y <= (player.position.y + player.size):
            return 1
        else:
            return -1
    else:
        return 0


def build_reward(player: Racket, ball: Ball) -> int:
    if player.position.x == ball.position.x:
        if player.position.y <= ball.position.y <= (player.position.y + player.size):
            return 10
        else:
            return -10
    elif player.position.y <= ball.position.y <= (player.position.y + player.size):
        return 1
    elif player.position.y > ball.position.y:
        return abs(ball.position.y - player.position.y) * -1
    elif (player.position.y + player.size) < ball.position.y:
        return abs(ball.position.y - (player.position.y + player.size)) * -1


def build_content(simulation: int, y_cache: List, player: Racket, ball: Ball, content: str) -> str:
    content = content + '\n' + str(simulation) + ';' + str(player.position.x) + ';' \
              + str(player.position.y) + ';' + str(ball.position.x) + ';' + str(ball.position.y) + \
              ';' + build_action(y_cache, player) + ';' + str(build_reward(player, ball))
    return content


def create_data_file(file: str, content: str):
    with open(file, "w") as f:
        f.write(content)


def start_game_simulations(file1: str, file2: str, render: bool = True):
    term = Terminal()
    file_path_player1 = file1
    train1_content = 'SIMID;STATEX;STATEY;BALLX;BALLY;ACTION;REWARD'
    file_path_player2 = file2
    train2_content = 'SIMID;STATEX;STATEY;BALLX;BALLY;ACTION;REWARD'
    for i in range(0, simulations):
        sim_id = i + 1
        controller = GameController(table_size, player_size, game_speed)
        controller.game.reset()
        controller.game.play = True
        player1_y_cache = []
        player2_y_cache = []
        player1_y_cache.append(controller.game.player1.position.y)
        player2_y_cache.append(controller.game.player2.position.y)
        print('\t\t\t\tSIMULATION STATE = ' + str(sim_id) + '/' + str(simulations) + ' ...')
        while controller.game.play:
            player1_y_cache.append(controller.game.player1.position.y)
            player2_y_cache.append(controller.game.player2.position.y)
            train1_content = build_content(sim_id, player1_y_cache, controller.game.player1,
                                           controller.game.ball, train1_content)
            train2_content = build_content(sim_id, player2_y_cache, controller.game.player2,
                                           controller.game.ball, train2_content)
            if render:
                with term.location(0, 0):
                    print(term.move(0, 0) + controller.game.render(), end='\r')
                    time.sleep(controller.game_speed)
            controller.game.play_game()
    create_data_file(file_path_player1, train1_content)
    create_data_file(file_path_player2, train2_content)
    print("\t\t\t\t\t\t\tDONE!")
