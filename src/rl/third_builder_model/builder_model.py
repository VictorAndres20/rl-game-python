from sklearn.neural_network import MLPRegressor
import pickle
import numpy as np
from typing import Optional

# UP: 0 0 1
# DOWN: 1 0 0


def build_model(file: str) -> Optional[MLPRegressor]:
    if file is None:
        return None
    else:
        with open(file, "rb") as f:
            model = pickle.load(f)
        return model


def predict(model: MLPRegressor, state_x: int, state_y: int, ball_x: int, ball_y: int) -> str:
    up_nn = np.array([state_x, state_y, ball_x, ball_y, 0, 0, 1]).reshape(1, -1)
    down_nn = np.array([state_x, state_y, ball_x, ball_y, 1, 0, 0]).reshape(1, -1)

    predict_up = model.predict(up_nn)
    predict_down = model.predict(down_nn)
    if predict_down > predict_up:
        return "DOWN"
    return "UP"
