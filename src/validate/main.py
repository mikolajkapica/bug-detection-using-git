import pickle
import pydriller

from src.models.data_processing import load_data
from src.validate.validate import validate_model_on_commits

GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"
SCALER_PATH = "../../trained_models/oversampling/scaler.pkl"
MODEL_PATH = "../../trained_models/oversampling/RandomForestClassifier.pkl"


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
        ("3ba9d4756509528dfed16ea4a1ab99ece9c4e610", normal_commit),
        ("d5d17f8e123d475746cb8be340fb3853af517c37", normal_commit),
        ("e09d1cb030f12e86efa14010c8541c49e1483cfe", normal_commit),
        ("5f3fd88b64a461e73327ffe5406a5062431c7f04", normal_commit),
        ("3e7c90919fb892ece6308fc6640430f70b282f2a", normal_commit),
        ("6d0c0bf8da592dc7fce57729564511ba3881cd81", buggy_commit),
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
