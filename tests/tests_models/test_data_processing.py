import pandas as pd

from src.models.data_processing import load_data, undersample, oversample, split_data


PREPROCESSED_DATASET_LOCATION = "../tests/test_data/commits_sample.csv"
PREPROCESSED_DATA = pd.read_csv(PREPROCESSED_DATASET_LOCATION)


def test_load_data():
    df = load_data(PREPROCESSED_DATASET_LOCATION)
    assert df.shape == (100, 9494)
    assert df.isnull().values.any() == False


def test_undersample():
    df = PREPROCESSED_DATA
    buggy_commits = df[df["is_bug"] == 1].shape[0]
    normal_commits = df[df["is_bug"] == 0].shape[0]
    df = undersample(df)
    assert df.shape == (2 * buggy_commits, 9494)


def test_oversample():
    df = PREPROCESSED_DATA
    buggy_commits = df[df["is_bug"] == 1].shape[0]
    normal_commits = df[df["is_bug"] == 0].shape[0]
    df = oversample(df)
    assert df.shape == (2 * normal_commits, 9494)


def test_split_data():
    df = PREPROCESSED_DATA
    X_train, X_test, y_train, y_test = split_data(df, 0.2, 0)
    assert X_train.shape[0] == 80
    assert X_test.shape[0] == 20
    assert y_train.shape[0] == 80
    assert y_test.shape[0] == 20
