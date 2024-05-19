import pickle
import pydriller

from src.models.data_processing import load_data
from src.validation.validate import validate_model_on_commits

GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"
SCALER_PATH = "../../preprocessed_dataset/scaler.pkl"
MODEL_PATH = "../../trained_models/oversampled/RandomForestClassifier.pkl"


def main() -> None:
    columns_needed = load_data(PREPROCESSED_DATASET).columns

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    repo = pydriller.Git(GIT_REPO_PATH)

    buggy_commit = True
    normal_commit = False

    commit_hashes_actual = [
        ("b782c41b6e85705857f1db103289d4de3e2c52af", normal_commit),
        ("46a1346ad498a17c56c56b7ea2608899a7327575", normal_commit),
        ("9271e595a00692f789a23cdb67b12a4c35ef6240", normal_commit),
        ("432ec1f82479a0fb85a62d783170fcc050901390", normal_commit),
        ("31c5fe5f634faf75bca527e0cdc5403f1c1cc7f4", buggy_commit),
        ("60a3edd6a2d7a454c9c30d8983e8a3eec1db4d4f", normal_commit),
        ("6622a7d3933c5f5a794e0b2561096de811fc98e6", buggy_commit),
        ("f4b5adc41dfa495037b9c17b0874444fe40e543d", buggy_commit),
        ("8627e7025912261882b32394f6ea467e791f4ef8", buggy_commit),
        ("9580c830fb091476a468aa1b54241dd7efa5c25d", buggy_commit),
    ]

    prediction_results = validate_model_on_commits(
        repo,
        commit_hashes_actual,
        columns_needed,
        model,
        scaler,
    )

    print(prediction_results)


if __name__ == "__main__":
    main()
