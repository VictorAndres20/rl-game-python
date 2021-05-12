import pandas as pd
from sklearn.neural_network import MLPRegressor
import pickle


def train_model(train_file: str) -> MLPRegressor:
    dataset = pd.read_csv(train_file, sep=";")

    print("\nDataset:")
    print(dataset.head(10))

    dataset.drop('SIMID', axis=1, inplace=True)

    x = dataset.drop('REWARD', axis=1)
    y = dataset['REWARD']

    from sklearn.preprocessing import OneHotEncoder
    enc = OneHotEncoder(handle_unknown='ignore')
    enc_df = pd.DataFrame(enc.fit_transform(x[['ACTION']]).toarray())
    x = x.join(enc_df)
    x = x.drop(['ACTION'], axis=1)

    print("\nDataset (after one hot encoding):")
    print(x.head(10))

    model = MLPRegressor(hidden_layer_sizes=(100, 75, 50, 25), activation='relu', solver='sgd',
                         learning_rate='adaptive', max_iter=500)
    model.fit(x, y)
    print(model.loss_)
    return model


def save_model(model_file: str, model: MLPRegressor):
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
