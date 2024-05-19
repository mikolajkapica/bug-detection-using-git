from typing import Callable
import pickle
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.tree import plot_tree

from src.models.models import Model


def load_data(preprocessed_dataset_location: str) -> pd.DataFrame:
    df = pd.read_csv(preprocessed_dataset_location)
    df = df.fillna(0)
    return df


def undersample(df: pd.DataFrame) -> pd.DataFrame:
    df_normal = df[df["is_bug"] == 0]
    df_buggy = df[df["is_bug"] == 1]
    df_normal = df_normal.sample(n=len(df_buggy), random_state=0)
    return pd.concat([df_normal, df_buggy])


def oversample(df: pd.DataFrame) -> pd.DataFrame:
    df_normal = df[df["is_bug"] == 0]
    df_buggy = df[df["is_bug"] == 1]
    if len(df_buggy) == 0:
        return df
    df_buggy = df_buggy.sample(n=len(df_normal), replace=True, random_state=0)
    return pd.concat([df_normal, df_buggy])


def split_data(df: pd.DataFrame, test_size: float, random_state: int) -> tuple:
    X = df.drop("is_bug", axis=1)
    y = df["is_bug"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def train_model(
    model: Model, X_train: pd.DataFrame, y_train: pd.DataFrame, save_location: str = ""
) -> Model:
    model.fit(X_train, y_train)

    if save_location:
        pickle.dump(
            model, open(f"{save_location}/{model.__class__.__name__}.pkl", "wb")
        )

    return model


def predict(model: Model, X_test: pd.DataFrame) -> pd.Series:
    return model.predict(X_test)


def generate_confusion_matrix(
    model: Model, y_test: pd.Series, y_pred: pd.Series, save_location: str = ""
) -> None:
    plt.figure(figsize=(12, 8))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
    plt.title(f"Confusion Matrix for {model.__class__.__name__}")

    if save_location:
        plt.savefig(f"{save_location}/{model.__class__.__name__}_confusion_matrix.png")

    plt.show()


def generate_classification_report(
    model: Model, y_test, y_pred, save_location: str = ""
) -> None:
    report = (
        "Classification Report for "
        + model.__class__.__name__
        + "\n"
        + classification_report(y_test, y_pred)
    )

    print(report)

    if save_location:
        with open(
            f"{save_location}/{model.__class__.__name__}_classification_report.txt",
            "w+",
        ) as file:
            file.write(report)


def plot_decision_tree(
    decision_tree_classifier: Model,
    save_location: str,
) -> None:
    plt.figure(figsize=(40, 30))
    plot_tree(decision_tree_classifier, filled=True)
    plt.title("Decision Tree")

    if save_location:
        plt.savefig(f"{save_location}/decision_tree.png")

    plt.show()


def models_testing(
    preprocessed_dataset_directory: str,
    models: list[Callable[[], Model]],
    test_size: float = 0.2,
    random_state: int = 0,
    sampling: str = "",
    save_models_location: str = "",
    save_confusion_matrix_location: str = "",
    save_report_location: str = "",
) -> None:
    df = load_data(preprocessed_dataset_directory)
    if sampling == "undersample":
        df = undersample(df)
    elif sampling == "oversample":
        df = oversample(df)

    X_train, X_test, y_train, y_test = split_data(df, test_size, random_state)

    for model in models:
        model = train_model(model(), X_train, y_train, save_models_location)
        y_pred = predict(model, X_test)
        generate_confusion_matrix(model, y_test, y_pred, save_confusion_matrix_location)
        generate_classification_report(model, y_test, y_pred, save_report_location)
