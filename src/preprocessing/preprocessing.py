import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

NORMAL_COMMITS_JSONL = "../../raw_dataset/normal_commits.jsonl"
BUGGY_COMMITS_JSONL = "../../raw_dataset/buggy_commits.jsonl"

NORMAL_COMMITS_PREPROCESSED_PATH = "../../preprocessed_data/normal_commits.jsonl"
BUGGY_COMMITS_PREPROCESSED_PATH = "../../preprocessed_data/buggy_commits.jsonl"


def drop_hash(df):
    df.drop("hash", axis=1, inplace=True)
    return df


def drop_outliers(df):
    mean = df["lines"].mean()
    std = df["lines"].std()
    df = df[df["lines"] < mean + 5 * std]
    df = df[df["lines"] > mean - 5 * std]
    return df


def normalization(df):
    scaler = StandardScaler()
    columns_to_normalize = [
        "deletions",
        "insertions",
        "lines",
        "files",
        "dmm_unit_size",
        "dmm_unit_complexity",
        "dmm_unit_interfacing",
    ]
    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    return df


def feature_engineering(df):
    df["ratio_insertions_deletions"] = df["insertions"] / df["deletions"]
    df["msg_length"] = df["msg"].apply(len)
    return df


def binary_encoding(df):
    df["is_bug"] = df["is_bug"].astype(int)
    return df


def one_hot_encoding_author_name(df):
    df = pd.get_dummies(df, columns=["author_name"])
    return df


def transformation_date(df):
    df["author_date"] = df["author_date"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z")
    )
    df["day_of_week"] = df["author_date"].apply(lambda x: x.weekday())
    df["hour_of_day"] = df["author_date"].apply(lambda x: x.hour)
    df.drop("author_date", axis=1, inplace=True)
    return df


def tf_idf_msg(df):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["msg"])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out()
    )
    df = pd.concat([df, tfidf_df], axis=1)
    return df


def preprocess(df):
    df = drop_hash(df)
    df = drop_outliers(df)
    df = normalization(df)
    df = feature_engineering(df)
    df = binary_encoding(df)
    df = one_hot_encoding_author_name(df)
    df = transformation_date(df)
    df = tf_idf_msg(df)
    return df


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)

    df = pd.read_json(NORMAL_COMMITS_JSONL, lines=True)
    df = preprocess(df)
