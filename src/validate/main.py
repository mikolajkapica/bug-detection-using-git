import pickle
import pydriller
import pandas as pd

from src.models.data_processing import load_data
from src.preprocessing.preprocessing import preprocess


GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"
SCALER_PATH = "../../scalers/scaler.pkl"
MODEL_PATH = "../../trained_models/oversampling/RandomForestClassifier.pkl"


def main() -> None:
    columns_needed = load_data(PREPROCESSED_DATASET).columns

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    repo = pydriller.Git(GIT_REPO_PATH)

    commit_hashes_actual = [
        ("3ba9d4756509528dfed16ea4a1ab99ece9c4e610", False),
        ("d5d17f8e123d475746cb8be340fb3853af517c37", False),
        ("e09d1cb030f12e86efa14010c8541c49e1483cfe", False),
        ("5f3fd88b64a461e73327ffe5406a5062431c7f04", False),
        ("3e7c90919fb892ece6308fc6640430f70b282f2a", False),
        ("6d0c0bf8da592dc7fce57729564511ba3881cd81", True),
    ]
    commit_hashes = [commit_hash for commit_hash, _ in commit_hashes_actual]
    y_actual = [is_bug for _, is_bug in commit_hashes_actual]
    commits = map(repo.get_commit, commit_hashes)
    commits_data = [
        {
            "hash": commit.hash,
            "msg": commit.msg,
            "author_name": commit.author.name,
            "author_date": str(commit.author_date),
            "author_timezone": commit.author_timezone,
            "merge": commit.merge,
            "deletions": commit.deletions,
            "insertions": commit.insertions,
            "lines": commit.lines,
            "files": commit.files,
            "dmm_unit_size": commit.dmm_unit_size,
            "dmm_unit_complexity": commit.dmm_unit_complexity,
            "dmm_unit_interfacing": commit.dmm_unit_interfacing,
            "is_bug": False,
        }
        for commit in commits
    ]

    df = pd.DataFrame(commits_data)
    df = preprocess(df, scaler)
    X_test = df.reindex(columns=columns_needed, fill_value=0)

    y_pred = model.predict(X_test)

    print(
        f"Predicted right: {sum([1 for i in range(len(y_pred)) if y_pred[i] == y_actual[i]])}/{len(y_pred)}"
    )


if __name__ == "__main__":
    main()
