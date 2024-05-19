import pandas as pd


def deserialize(
    normal_commits_path: str, buggy_commits_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    normal_commits = pd.read_json(normal_commits_path, lines=True)
    buggy_commits = pd.read_json(buggy_commits_path, lines=True)
    return normal_commits, buggy_commits
