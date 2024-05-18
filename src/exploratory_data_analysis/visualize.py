import pandas as pd
import graphs

NORMAL_COMMITS_JSONL = "../../raw_dataset/normal_commits.jsonl"
BUGGY_COMMITS_JSONL = "../../raw_dataset/buggy_commits.jsonl"

if __name__ == "__main__":
    normal_df = pd.read_json(NORMAL_COMMITS_JSONL, lines=True)
    buggy_df = pd.read_json(BUGGY_COMMITS_JSONL, lines=True)

    # print quantity of commits
    print(f"Normal commits: {len(normal_df)}")
    print(f"Buggy commits: {len(buggy_df)}")

    normal_lines_95 = normal_df["lines"].quantile(0.95)
    normal_df = normal_df[normal_df["lines"] < normal_lines_95]
    buggy_df = buggy_df[buggy_df["lines"] < normal_lines_95]

    graphs.means_of_lines(normal_df, buggy_df)
    graphs.medians_of_lines(normal_df, buggy_df)
    graphs.biggest_commits(pd.concat([normal_df, buggy_df]))
