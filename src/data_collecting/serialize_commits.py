import json
import pydriller


def serialize(
    git_repo_path: str,
    buggy_hashes_path: str,
    normal_commits_path: str,
    buggy_commits_path: str,
    quantity_of_commits: int,
) -> None:
    repo = pydriller.Git(git_repo_path)
    all_commits = list(repo.get_list_commits())[:quantity_of_commits]

    with open(buggy_hashes_path, "r") as f:
        buggy_commits = sorted([commit.strip() for commit in f.readlines()])

    normal_commits_path = open(normal_commits_path, "a")
    buggy_commits_path = open(buggy_commits_path, "a")

    for i, commit in enumerate(all_commits):
        is_bug = commit.hash in buggy_commits
        commit_data = {
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
            "is_bug": is_bug,
        }

        if is_bug:
            json.dump(commit_data, buggy_commits_path)
            buggy_commits_path.write("\n")
        else:
            json.dump(commit_data, normal_commits_path)
            normal_commits_path.write("\n")

    buggy_commits_path.close()
    normal_commits_path.close()
