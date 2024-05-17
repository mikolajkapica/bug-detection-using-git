from src.data_collecting.gather_buggy_hashes import gather
from src.data_collecting.deserialize_commits import deserialize
from src.data_collecting.serialize_commits import serialize

GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
BUGGY_HASHES_PATH = "../dataset/buggy_hashes_02-05-2024_02-00.txt"
NORMAL_COMMITS_PATH = "../dataset/normal_commits.jsonl"
BUGGY_COMMITS_PATH = "../dataset/bug_commits.jsonl"


def main():
    # Save all buggy commit hashes to a file
    gather(GIT_REPO_PATH)

    # Serialize all commits to jsonl files (normal and buggy commits to separate files)
    # serialize(
    #     GIT_REPO_PATH,
    #     BUGGY_HASHES_PATH,
    #     NORMAL_COMMITS_PATH,
    #     BUGGY_COMMITS_PATH,
    #     10000,
    # )

    # Deserialize the jsonl files to lists of dictionaries
    # normal_commits, bug_commits = deserialize(normal_commits_path, buggy_commits_path)


if __name__ == "__main__":
    main()
