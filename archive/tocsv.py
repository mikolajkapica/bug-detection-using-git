import json

input_file1 = "../data_objects/buggy_commits.jsonl"
input_file2 = "../data_objects/normal_commits.jsonl"
output_file = "../archive/data_objects/commits.csv"

data = []

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

f = open(output_file, "w", encoding="utf-8")

with open(input_file1, "r") as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        data = json.loads(line)
        for column in columns:
            if isinstance(data[column], str):
                data[column] = (
                    '"' + data[column].replace("\n", "\\n").replace('"', "'") + '"'
                )
        f.write(
            ",".join([str(data[column]).replace("\n", "\\n") for column in columns])
            + "\n"
        )

with open(input_file2, "r") as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        data = json.loads(line)
        for column in columns:
            if isinstance(data[column], str):
                data[column] = (
                    '"' + data[column].replace("\n", "\\n").replace('"', "'") + '"'
                )
        f.write(
            ",".join([str(data[column]).replace("\n", "\\n") for column in columns])
            + "\n"
        )

print(f"Data successfully written to {output_file}")
