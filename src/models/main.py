from src.models.data_processing import pipeline
from src.models.models import models

PREPROCESSED_DATASET_DIRECTORY = "../../preprocessed_dataset"


def main() -> None:
    pipeline(
        PREPROCESSED_DATASET_DIRECTORY,
        models,
        save_location="../../graphs/results",
    )


if __name__ == "__main__":
    main()
