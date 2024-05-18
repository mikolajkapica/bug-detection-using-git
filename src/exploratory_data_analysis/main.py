from datetime import datetime
import pandas as pd
import os

from src.exploratory_data_analysis import plotter

NORMAL_COMMITS_JSONL = "../../raw_dataset/normal_commits.jsonl"
BUGGY_COMMITS_JSONL = "../../raw_dataset/buggy_commits.jsonl"


def main() -> None:
    normal_df = pd.read_json(NORMAL_COMMITS_JSONL, lines=True)
    buggy_df = pd.read_json(BUGGY_COMMITS_JSONL, lines=True)

    # exclude commits with more than unusual number of lines
    lines_non_outliers = pd.concat([normal_df, buggy_df])["lines"].quantile(0.95)
    normal_df = normal_df[normal_df["lines"] < lines_non_outliers]
    buggy_df = buggy_df[buggy_df["lines"] < lines_non_outliers]

    # exclude merge commits
    normal_df = normal_df[normal_df["merge"] == False]
    buggy_df = buggy_df[buggy_df["merge"] == False]

    # create directory to save plots
    location = "../../graphs/graphs_" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs(location, exist_ok=True)

    # create plots
    p = plotter.Plotter(normal_df, buggy_df, location, is_save=True)
    p.count_commits()
    p.means_of_lines()
    p.medians_of_lines()
    p.biggest_commits(n=20)
    p.authors_ratio()
    p.weekday_ratio()
    p.hour_ratio()
    p.correlation_matrix()
    p.distribution_lines()


if __name__ == "__main__":
    main()
