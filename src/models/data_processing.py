from typing import Callable
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
)
from src.models.models import Model


def load_data(preprocessed_dataset_directory: str) -> pd.DataFrame:
    df_normal = pd.read_csv(f"{preprocessed_dataset_directory}/normal_commits.csv")
    df_buggy = pd.read_csv(f"{preprocessed_dataset_directory}/buggy_commits.csv")
    df = pd.concat([df_normal, df_buggy])
    df = df.fillna(0)
    return df


def split_data(df: pd.DataFrame, test_size: float, random_state: int) -> tuple:
    X = df.drop("is_bug", axis=1)
    y = df["is_bug"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def train_model(model: Model, X_train: pd.DataFrame, y_train: pd.DataFrame) -> Model:
    model.fit(X_train, y_train)
    return model


def predict(model: Model, X_test: pd.DataFrame) -> Series:
    return model.predict(X_test)


def plot_confusion_matrix(
    model: Model, y_test: Series, y_pred: Series, save_location: str
) -> None:
    plt.figure(figsize=(12, 8))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
    plt.title(f"Confusion Matrix for {model.__class__.__name__}")

    if save_location:
        plt.savefig(f"{save_location}/{model.__class__.__name__}_confusion_matrix.png")

    plt.show()


def get_classification_report(model: Model, y_test, y_pred) -> str:
    return (
        "Classification Report for "
        + model.__class__.__name__
        + "\n"
        + classification_report(y_test, y_pred)
    )


def pipeline(
    preprocessed_dataset_directory: str,
    models: list[Callable[[], Model]],
    test_size: float = 0.2,
    random_state: int = 0,
    save_location: str = "",
) -> None:
    df = load_data(preprocessed_dataset_directory)
    X_train, X_test, y_train, y_test = split_data(df, test_size, random_state)
    for model in models:
        model = train_model(model(), X_train, y_train)
        y_pred = predict(model, X_test)
        plot_confusion_matrix(model, y_test, y_pred, save_location)
        print(get_classification_report(model, y_test, y_pred))
