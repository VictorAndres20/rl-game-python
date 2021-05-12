from src.app.controllers.game_controller import GameController
from src.rl.first_generate_data.generate_game_data import start_game_simulations
from src.rl.second_train_model.train_models import train_model, save_model
from typing import List
from sklearn.neural_network import MLPRegressor


def start_simple_game():
    controller = GameController(21, 3, 0.3)
    controller.start_game_simple_loop()


def start_generate_data():
    file_path_player1 = './train1_data.csv'
    file_path_player2 = './train2_data.csv'
    start_game_simulations(file_path_player1, file_path_player2, render=False)


def generate_save_models() -> List[MLPRegressor]:
    file_path_player1 = './train1_data.csv'
    file_path_player2 = './train2_data.csv'
    model1_file = './trained_model_1'
    model2_file = './trained_model_2'
    model1 = train_model(file_path_player1)
    model2 = train_model(file_path_player2)
    save_model(model1_file, model1)
    save_model(model2_file, model2)
    return [model1, model2]


def start_ai_game():
    model1_file = './trained_model_1'
    model2_file = './trained_model_2'
    controller = GameController(21, 3, 0.3,
                                p1_file_model=model1_file, p2_file_model=model2_file)
    controller.start_game_simple_loop()


if __name__ == '__main__':
    # start_simple_game()
    # start_generate_data()
    # generate_save_models()
    start_ai_game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
