import pydriller
import re
from datetime import datetime as dt

RE_FIX_COMMIT = re.compile(r"(?i)(fix(e[sd])?|bug(s)?)")
GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"

DATASET_DIRECTORY = "./dataset"
DATASET_BASENAME = "bugs"
DATASET_EXTENSION = ".txt"


if __name__ == "__main__":
    repo = pydriller.Git(GIT_REPO_PATH)

    buggy_commits = {
        commit_hash
        for fix_commit in repo.get_list_commits()
        if RE_FIX_COMMIT.match(fix_commit.msg)
        for hashes in repo.get_commits_last_modified_lines(fix_commit).values()
        for commit_hash in hashes
    }

    file_name = (
        DATASET_DIRECTORY
        + "/"
        + DATASET_BASENAME
        + "_"
        + dt.now().strftime("%d-%m-%Y_%H-%M")
        + DATASET_EXTENSION
    )

    with open(file_name, "w", newline="") as f:
        for commit in buggy_commits:
            f.write(f"{commit}\n")
