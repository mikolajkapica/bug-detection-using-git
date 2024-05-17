from datetime import datetime as dt
import pydriller
import re

RE_FIX_COMMIT = re.compile(r"(?i)(fix(e[sd])?|bug(s)?)")

DATASET_DIRECTORY = "../dataset"
DATASET_BASENAME = "buggy_hashes"
DATASET_EXTENSION = ".txt"


def gather(git_repo_path: str) -> None:
    repo = pydriller.Git(git_repo_path)

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

    with open(file_name, "w+", newline="") as f:
        for commit in buggy_commits:
            f.write(f"{commit}\n")
