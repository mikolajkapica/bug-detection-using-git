import pickle
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier


def feature_importances(
    decision_tree_classifier: DecisionTreeClassifier,
    model_location: str,
    preprocessed_dataset_location: str,
) -> list[str]:
    with open(model_location, "rb") as f:
        preprocessed_data = pd.read_csv(preprocessed_dataset_location)
        indices = np.argsort(decision_tree_classifier.feature_importances_)[-10:]
        cols = preprocessed_data.columns
        return cols[indices].tolist()


def get_important_features_dt(
    save_models_location: str, preprocessed_dataset: str
) -> list[str]:
    with open(f"{save_models_location}/DecisionTreeClassifier.pkl", "rb") as f:
        model = pickle.load(f)
        features = feature_importances(
            model,
            f"{save_models_location}/DecisionTreeClassifier.pkl",
            preprocessed_dataset,
        )
        return features
