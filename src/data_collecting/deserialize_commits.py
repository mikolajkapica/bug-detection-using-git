import json


def deserialize(
    normal_commits_path: str, buggy_commits_path: str
) -> tuple[list[dict], list[dict]]:
    with open(normal_commits_path, "r") as f:
        normal_commits = [json.loads(line) for line in f.readlines()]
    with open(buggy_commits_path, "r") as f:
        buggy_commits = [json.loads(line) for line in f.readlines()]

    return normal_commits, buggy_commits
