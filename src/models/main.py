from src.models.data_processing import (
    models_testing,
    plot_decision_tree,
    train_and_save,
)
from src.models.models import models


PREPROCESSED_DATASET_DIRECTORY = "../../preprocessed_dataset"


def main() -> None:
    models_testing(
        PREPROCESSED_DATASET_DIRECTORY,
        models,
        # save_location="../../graphs/results",
        sampling="oversample",
    )
    # train_and_save(models[0], PREPROCESSED_DATASET_DIRECTORY, "../../trained_models")


if __name__ == "__main__":
    main()
