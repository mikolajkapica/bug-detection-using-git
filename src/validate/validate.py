import pandas as pd
import pydriller
from src.models.models import Model
from src.preprocessing.preprocessing import preprocess


def validate_commit(
    git_repo_path: str,
    repo_commit_hash: str,
    model: Model,
    is_bug: bool,
    x_train_columns: list,
) -> bool:
    repo = pydriller.Git(git_repo_path)
    commit = repo.get_commit(repo_commit_hash)

    X_test = pd.DataFrame(
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
            "is_bug": is_bug,
        },
        index=[0],
    )
    X_test = preprocess(X_test)
    y_test = X_test["is_bug"]
    X_test = X_test.drop(columns=["is_bug"], axis=1)
    # see difference between x_train_columns and X_test.columns
    print(f"X_train_columns: {x_train_columns}")
    print(f"X_test_columns: {X_test.columns}")
    X_test = X_test.reindex(columns=x_train_columns, fill_value=0)

    y_pred = model.predict(X_test)
    print(f"Predicted: {y_pred[0]}")
    print(f"Actual: {y_test[0]}")
    print(f"Expected: {is_bug}")

    return y_pred[0] == is_bug
