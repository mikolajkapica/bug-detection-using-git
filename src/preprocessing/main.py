import pandas as pd
from src.preprocessing.preprocessing import preprocess

NORMAL_COMMITS_JSONL = "../../raw_dataset/normal_commits.jsonl"
BUGGY_COMMITS_JSONL = "../../raw_dataset/buggy_commits.jsonl"
PREPROCESSED_COMMITS_PATH = "../../preprocessed_dataset/commits.csv"
SCALER_SAVE_LOCATION = "../../preprocessed_dataset/scaler.pkl"


def main() -> None:
    normal_commits = pd.read_json(NORMAL_COMMITS_JSONL, lines=True)
    buggy_commits = pd.read_json(BUGGY_COMMITS_JSONL, lines=True)
    commits = pd.concat([normal_commits, buggy_commits])
    commits.reset_index(drop=True, inplace=True)

    preprocessed_commits = preprocess(
        commits,
        scaler=None,
        scaler_save_location=SCALER_SAVE_LOCATION,
    )
    # preprocessed_commits.to_csv(PREPROCESSED_COMMITS_PATH, index=False)


if __name__ == "__main__":
    main()
