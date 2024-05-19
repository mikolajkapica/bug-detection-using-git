import pickle
import json

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.models.data_processing import (
    load_data,
    oversample,
    train_model,
    split_data,
    plot_confusion_matrix,
    get_classification_report,
    undersample,
)
import pydriller

from src.preprocessing.preprocessing import preprocess
from src.validate.validate import validate_commit


GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
PREPROCESSED_DATASET = "../../preprocessed_dataset/commits.csv"
TRAINED_MODELS_PATH = "../../trained_models/oversampling"
MODEL_NAME = "RandomForestClassifier"


def main() -> None:
    df = load_data(PREPROCESSED_DATASET)
    X_train, X_test, y_train, y_test = split_data(df, 0.2, 0)
    X_train_columns = X_train.columns
    # model = train_model(RandomForestClassifier(), X_train, y_train)
    # y_pred = model.predict(X_test)
    # plot_confusion_matrix(model, y_test, y_pred, TRAINED_MODELS_PATH)
    # print(get_classification_report(model, y_test, y_pred))
    with open(f"{TRAINED_MODELS_PATH}/{MODEL_NAME}.pkl", "rb") as f:
        model = pickle.load(f)

    # WORKS
    # data = pd.read_json("../../raw_dataset/normal_commits.jsonl", lines=True)
    # data = preprocess(data)
    # X_test = data.drop(columns=["is_bug"], axis=1)
    # X_test = data.reindex(columns=X_train_columns, fill_value=0)
    # y_test = data["is_bug"]
    # y_pred = model.predict(X_test)
    # print(
    #     f"Predicted right: {sum([1 for i in range(len(y_pred)) if y_pred[i] == y_test.iloc[i]])}/{len(y_pred)}"
    # )

    # DOESNT WORK
    # with open("../../raw_dataset/normal_commits.jsonl") as f:
    #     commit_hashes = pd.read_json(f, lines=True)["hash"].tolist()[:100]

    repo = pydriller.Git(GIT_REPO_PATH)
    commit_hashes = [
        "3ba9d4756509528dfed16ea4a1ab99ece9c4e610",
        "d5d17f8e123d475746cb8be340fb3853af517c37",
        "e09d1cb030f12e86efa14010c8541c49e1483cfe",
        "5f3fd88b64a461e73327ffe5406a5062431c7f04",
        "3e7c90919fb892ece6308fc6640430f70b282f2a",
        "6d0c0bf8da592dc7fce57729564511ba3881cd81",
    ]

    commits = map(lambda commit_hash: repo.get_commit(commit_hash), commit_hashes)

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
            "is_bug": False,
        }
        for commit in commits
    ]
    df = pd.DataFrame(commits_data)
    scaler = pickle.load(open(f"../../scalers/scaler.pkl", "rb"))
    df = preprocess(df, scaler)
    # save the pd to csv
    df.to_csv("test.csv")
    X_test = df.reindex(columns=X_train_columns, fill_value=0)
    y_pred = model.predict(X_test)
    y_actual = [False, False, False, False, False, True]
    print(
        f"Predicted right: {sum([1 for i in range(len(y_pred)) if y_pred[i] == y_actual[i]])}/{len(y_pred)}"
    )


if __name__ == "__main__":
    main()

    # y_pred = model.predict(X_train)
    # how many it got right out of the total
    # print(f"Predicted: {y_pred}")
    # print(
    #     f"Predicted right: {sum([1 for i in range(len(y_pred)) if y_pred[i] == y_train.iloc[i]])}/{len(y_pred)}"
    # )

    # with open("../../raw_dataset/normal_commits.jsonl") as f:
    #     commit_hashes = pd.read_json(f, lines=True)["hash"].tolist()
    #
    # repo = pydriller.Git(GIT_REPO_PATH)
    # commits = [repo.get_commit(h) for h in commit_hashes[:100]]
    # commits = [
    #     {
    #         "hash": commit.hash,
    #         "msg": commit.msg,
    #         "author_name": commit.author.name,
    #         "author_date": str(commit.author_date),
    #         "author_timezone": commit.author_timezone,
    #         "merge": commit.merge,
    #         "deletions": commit.deletions,
    #         "insertions": commit.insertions,
    #         "lines": commit.lines,
    #         "files": commit.files,
    #         "dmm_unit_size": commit.dmm_unit_size,
    #         "dmm_unit_complexity": commit.dmm_unit_complexity,
    #         "dmm_unit_interfacing": commit.dmm_unit_interfacing,
    #         "is_bug": False,
    #     }
    #     for commit in commits
    # ]
    # X_test = pd.DataFrame(commits)
    # X_test = preprocess(X_test)
    # y_test = X_test["is_bug"]
    # X_test = X_test.drop(columns=["is_bug"], axis=1)
    # print(f"X_train_columns: {X_train_columns}")
    # print(f"X_test_columns: {X_test.columns}")
    # X_test = X_test.reindex(columns=X_train_columns, fill_value=0)
    # y_pred = model.predict(X_test)
    # print(
    #     f"Predicted right: {sum([1 for i in range(len(y_pred)) if y_pred[i] == y_test.iloc[i]])}/{len(y_test)}"
    # )

    # print(f"Predicted: {y_pred}")
    # print(f"Written: {y_test}")
    # print(f"Expected: {[data[1] for data in validation_data]}")
    # df = load_data(PREPROCESSED_DATASET_DIRECTORY)
    # X_train, _, _, _ = split_data(df, 0.2, 0)
    # X_train_columns = X_train.columns
    #
    # commit_validations = [
    #     validate_commit(
    #         GIT_REPO_PATH,
    #         commit_hash,
    #         model,
    #         is_buggy,
    #         X_train_columns,
    #     )
    #     for commit_hash, is_buggy in validation_data
    # ]
    #
    # for data, validation in zip(validation_data, commit_validations):
    #     print(
    #         f"\033[92mCommit {data[0]} correct validation\033[0m"
    #         if validation
    #         else f"\033[91mCommit {data[0]} incorrect validation\033[0m"
    #     )
