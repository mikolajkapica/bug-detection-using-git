import pydriller
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.preprocessing.preprocessing import preprocess
from src.models.models import Model


def validate_model_on_commits(
    repo: pydriller.Git,
    commit_hashes_actual: list[tuple[str, bool]],
    columns_needed: list[str],
    model: Model,
    scaler: StandardScaler,
) -> str:
    commit_hashes = [commit_hash for commit_hash, _ in commit_hashes_actual]

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
            "is_bug": False,  # Placeholder
        }
        for commit in commits
    ]

    df = pd.DataFrame(commits_data)
    df = preprocess(df, scaler)
    X_test = df.reindex(columns=columns_needed, fill_value=0).drop(columns=["is_bug"])
    y_pred = model.predict(X_test)

    prediction_results = ""
    base_color = "\033[0m"
    red = "\033[91m"
    green = "\033[92m"
    for i, (commit_hash, is_bug) in enumerate(commit_hashes_actual):
        good_prediction = y_pred[i] == is_bug
        color = green if good_prediction else red
        predicted = "buggy" if y_pred[i] else "normal"
        actual = "buggy" if is_bug else "normal"
        prediction_results += f"{color} Commit hash: {commit_hash}: Predicted: {predicted}, Actual: {actual}{base_color}\n"

    return prediction_results
