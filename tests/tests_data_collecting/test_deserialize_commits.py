from src.data_collecting.deserialize_commits import deserialize


def test_deserialize():
    normal_commits, buggy_commits = deserialize(
        "../tests/test_data/normal_commits.jsonl",
        "../tests/test_data/buggy_commits.jsonl",
    )
    assert normal_commits.shape == (50, 14)
    assert buggy_commits.shape == (30, 14)
    columns = [
        "hash",
        "msg",
        "author_name",
        "author_date",
        "author_timezone",
        "merge",
        "deletions",
        "insertions",
        "lines",
        "files",
        "dmm_unit_size",
        "dmm_unit_complexity",
        "dmm_unit_interfacing",
        "is_bug",
    ]
    assert normal_commits.columns.tolist() == columns
    assert buggy_commits.columns.tolist() == columns
    assert normal_commits["is_bug"].sum() == 0
    assert buggy_commits["is_bug"].sum() == 30
    assert (
        normal_commits["msg"][0]
        == "gulp-symdest does not preserve links on electron (fixes #2)"
    )
    assert buggy_commits["msg"][0] == "Hello Code"
