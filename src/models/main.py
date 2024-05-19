from src.models.data_processing import models_testing
from src.models.models import models

PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"
SAVE_MODELS_LOCATION = "../../trained_models/oversampling"
SAVE_CONFUSION_MATRIX_LOCATION = "../../graphs/results_oversampling"
SAVE_CLASSIFICATION_REPORT_LOCATION = "../../classification_reports"


def main() -> None:
    models_testing(
        PREPROCESSED_DATASET,
        models,
        save_models_location=SAVE_MODELS_LOCATION,
        save_confusion_matrix_location=SAVE_CONFUSION_MATRIX_LOCATION,
        save_report_location=SAVE_CLASSIFICATION_REPORT_LOCATION,
        sampling="oversample",
    )


if __name__ == "__main__":
    main()
