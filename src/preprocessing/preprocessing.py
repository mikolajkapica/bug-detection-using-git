import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def drop_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["lines"] < df["lines"].quantile(0.99)]
    return df


def normalization(df: pd.DataFrame) -> pd.DataFrame:
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
    df = df.astype({column: float for column in columns_to_normalize})
    df.loc[:, columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df["ratio_insertions_deletions"] = df["insertions"] / df["lines"]
    df["msg_length"] = df["msg"].apply(len)
    return df


def binary_encoding(df: pd.DataFrame) -> pd.DataFrame:
    df["merge"] = df["merge"].astype(int)
    df["is_bug"] = df["is_bug"].astype(int)
    return df


def one_hot_encoding_author_name(df: pd.DataFrame) -> pd.DataFrame:
    pd.concat([df, pd.get_dummies(df["author_name"])], axis=1)
    df = df.drop("author_name", axis=1)
    return df


def transformation_date(df: pd.DataFrame) -> pd.DataFrame:
    df["author_date"] = df["author_date"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z")
    )
    df["day_of_week"] = df["author_date"].apply(lambda x: x.weekday())
    df["hour_of_day"] = df["author_date"].apply(lambda x: x.hour)
    df.drop("author_date", axis=1, inplace=True)
    df.drop("author_timezone", axis=1, inplace=True)
    return df


def tf_idf_msg(df: pd.DataFrame) -> pd.DataFrame:
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["msg"])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out()
    )
    tfidf_df.columns = [f"{column}_tfidf" for column in tfidf_df.columns]
    df = pd.concat([df, tfidf_df], axis=1)
    df = df.drop("msg", axis=1)
    return df


def dmm_fill_na_with_mean(df):
    df["dmm_unit_size"] = df["dmm_unit_size"].fillna(df["dmm_unit_size"].mean())
    df["dmm_unit_complexity"] = df["dmm_unit_complexity"].fillna(
        df["dmm_unit_complexity"].mean()
    )
    df["dmm_unit_interfacing"] = df["dmm_unit_interfacing"].fillna(
        df["dmm_unit_interfacing"].mean()
    )
    return df


def drop_merge_commits(df):
    df = df[df["merge"] == 0]
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop("hash", axis=1)
    df = drop_outliers(df)
    df = feature_engineering(df)
    df = binary_encoding(df)
    df = one_hot_encoding_author_name(df)
    df = transformation_date(df)
    df = tf_idf_msg(df)
    df = normalization(df)
    df = dmm_fill_na_with_mean(df)
    df = drop_merge_commits(df)
    return df
