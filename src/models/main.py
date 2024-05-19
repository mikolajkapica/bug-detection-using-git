from src.models.data_processing import (
    models_testing,
    plot_decision_tree,
    train_and_save,
)
from src.models.models import models


PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"


def main() -> None:
    models_testing(
        PREPROCESSED_DATASET,
        models,
        save_models_location="../../trained_models/oversampling",
        save_confusion_matrix_location="../../graphs/results_oversampling",
        save_classification_report_location="../../classification_reports",
        sampling="oversample",
    )
    # train_and_save(models[0], PREPROCESSED_DATASET_DIRECTORY, "../../trained_models")


if __name__ == "__main__":
    main()
