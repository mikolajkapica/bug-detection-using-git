from src.models.data_processing import models_testing
from src.models.models import models

PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"

SAMPLING = "oversampled"
SAVE_MODELS_LOCATION = f"../../trained_models/{SAMPLING}"
SAVE_CONFUSION_MATRIX_LOCATION = f"../../models_comparison/{SAMPLING}"
SAVE_CLASSIFICATION_REPORT_LOCATION = f"../../models_comparison/{SAMPLING}"


def main() -> None:
    models_testing(
        PREPROCESSED_DATASET,
        models,
        save_models_location=SAVE_MODELS_LOCATION,
        save_confusion_matrix_location=SAVE_CONFUSION_MATRIX_LOCATION,
        save_report_location=SAVE_CLASSIFICATION_REPORT_LOCATION,
        sampling=SAMPLING,
    )


if __name__ == "__main__":
    main()
