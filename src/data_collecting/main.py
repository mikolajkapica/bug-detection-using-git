from datetime import datetime

from src.data_collecting.gather_buggy_hashes import gather
from src.data_collecting.serialize_commits import serialize
from src.data_collecting.deserialize_commits import deserialize


DATASET_DIRECTORY = "../../dataset"
NOW = datetime.now().strftime("%d-%m-%Y_%H-%M")

GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
BUGGY_HASHES_PATH = f"{DATASET_DIRECTORY}/buggy_hashes_{NOW}.txt"
NORMAL_COMMITS_PATH = f"{DATASET_DIRECTORY}/normal_commits.jsonl"
BUGGY_COMMITS_PATH = f"{DATASET_DIRECTORY}/buggy_commits.jsonl"
QUANTITY_OF_COMMITS = 10000


def main():
    # Save all buggy commit hashes to a file
    gather(GIT_REPO_PATH, DATASET_DIRECTORY)

    # Serialize all commits to jsonl files (normal and buggy commits to separate files)
    serialize(
        GIT_REPO_PATH,
        BUGGY_HASHES_PATH,
        NORMAL_COMMITS_PATH,
        BUGGY_COMMITS_PATH,
        QUANTITY_OF_COMMITS,
    )

    # # Deserialize the jsonl files to lists of dictionaries
    # normal_commits, bug_commits = deserialize(NORMAL_COMMITS_PATH, BUGGY_COMMITS_PATH)


if __name__ == "__main__":
    main()
