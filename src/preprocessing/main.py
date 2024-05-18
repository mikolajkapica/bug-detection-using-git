import pandas as pd
from src.preprocessing.preprocessing import preprocess

NORMAL_COMMITS_JSONL = "../../raw_dataset/normal_commits.jsonl"
BUGGY_COMMITS_JSONL = "../../raw_dataset/buggy_commits.jsonl"

NORMAL_COMMITS_PREPROCESSED_PATH = "../../preprocessed_dataset/normal_commits.csv"
BUGGY_COMMITS_PREPROCESSED_PATH = "../../preprocessed_dataset/buggy_commits.csv"


def main() -> None:
    normal_commits = pd.read_json(NORMAL_COMMITS_JSONL, lines=True)
    buggy_commits = pd.read_json(BUGGY_COMMITS_JSONL, lines=True)

    preprocess(normal_commits).to_csv(NORMAL_COMMITS_PREPROCESSED_PATH, index=False)
    preprocess(buggy_commits).to_csv(BUGGY_COMMITS_PREPROCESSED_PATH, index=False)


if __name__ == "__main__":
    main()
