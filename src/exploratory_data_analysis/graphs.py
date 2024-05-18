import seaborn as sns
import matplotlib.pyplot as plt
from typing import Iterable
from collections import Counter

import pandas as pd

sns.set_theme(style="whitegrid")

RED = "#ff3b30"
YELLOW = "#ffcc00"
GREEN = "#34c759"
BLUE = "#007aff"
PURPLE = "#5856d6"
ORANGE = "#ff9500"
INDIGO = "#5856d6"
TEAL = "#5ac8fa"
PINK = "#ff2d55"
PALETTE = [RED, YELLOW, GREEN, BLUE, PURPLE, ORANGE, INDIGO, TEAL, PINK]
sns.set_palette(sns.color_palette(PALETTE))

degrees_of_blue = {
    0: "#007aff",
    1: "#0a84ff",
    2: "#1e8eff",
    3: "#3498db",
    4: "#4da6ff",
    5: "#5ac8fa",
    6: "#6bcbff",
    7: "#7bc4ff",
    8: "#8ec6ff",
    9: "#a5d8ff",
}

SIZE_WIDTH = 8
SIZE_HEIGHT = 6


def means_of_lines(normal_commits: pd.DataFrame, buggy_commits: pd.DataFrame) -> None:
    normal_lines_mean = normal_commits["lines"].mean()
    buggy_lines_mean = buggy_commits["lines"].mean()

    fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
    sns.barplot(
        x=["Normal commits", "Buggy commits"],
        y=[normal_lines_mean, buggy_lines_mean],
        hue=["Normal commits", "Buggy commits"],
        palette=[GREEN, RED],
        ax=ax,
    )

    margin = 0.3
    plt.text(0, normal_lines_mean + margin, f"{normal_lines_mean:.2f} LOC", ha="center")
    plt.text(1, buggy_lines_mean + margin, f"{buggy_lines_mean:.2f} LOC", ha="center")
    plt.title("Mean of lines in normal commits and buggy commits")
    plt.show()


def medians_of_lines(normal_commits: pd.DataFrame, buggy_commits: pd.DataFrame) -> None:
    normal_lines_median = normal_commits["lines"].median()
    buggy_lines_median = buggy_commits["lines"].median()

    fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
    sns.barplot(
        x=["Normal commits", "Buggy commits"],
        y=[normal_lines_median, buggy_lines_median],
        hue=["Normal commits", "Buggy commits"],
        palette=[GREEN, RED],
        ax=ax,
    )

    margin = 0.3
    plt.text(
        0, normal_lines_median + margin, f"{normal_lines_median:.2f} LOC", ha="center"
    )
    plt.text(
        1, buggy_lines_median + margin, f"{buggy_lines_median:.2f} LOC", ha="center"
    )
    plt.title("Median of lines in normal commits and buggy commits")
    plt.show()


def biggest_commits(
    all_commits: pd.DataFrame, n: int = 10, logarithmic: bool = False
) -> None:
    biggest_commits = all_commits.nlargest(n, "lines").sort_values("lines")
    messages = [
        f"{msg[:20]}..." if len(msg) > 20 else msg for msg in biggest_commits["msg"]
    ]

    fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
    sns.barplot(
        x=messages,
        y=biggest_commits["lines"],
        legend=False,
        hue=messages,
        palette=[color for color in degrees_of_blue.values()],
        ax=ax,
    )

    plt.title("Biggest commits")
    plt.xlabel("Commit message")
    plt.ylabel("Lines of code")
    plt.xticks(rotation=-45, ha="left")
    plt.grid(axis="y")
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def authors_ratio(all_commits: Iterable, bugs: Iterable, n: int = 10) -> None:
    author_commits = Counter([commit.author.name for commit in all_commits])
    author_bugs = Counter([bug.author.name for bug in bugs])

    authors = sorted(author_commits.keys(), key=lambda x: author_commits[x])[::-1][:n]
    commits = [author_commits[author] for author in authors]
    bugs = [author_bugs[author] for author in authors]

    sns.barplot(x=authors, y=commits, label="All commits", palette=PALETTE)
    sns.barplot(x=authors, y=bugs, label="Bug commits", palette=PALETTE)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.show()


def days_of_the_week(all_commits: Iterable, bugs: Iterable) -> None:
    days_commits = Counter([commit.committer_date.weekday() for commit in all_commits])
    days_bugs = Counter([bug.committer_date.weekday() for bug in bugs])

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    commits = [days_commits[i] for i in range(7)]
    bugs = [days_bugs[i] for i in range(7)]

    sns.barplot(x=days, y=commits, label="All commits", palette=PALETTE)
    sns.barplot(x=days, y=bugs, label="Bug commits", palette=PALETTE)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.show()


def hours_of_the_day(all_commits: Iterable, bugs: Iterable) -> None:
    hours_commits = Counter([commit.committer_date.hour for commit in all_commits])
    hours_bugs = Counter([bug.committer_date.hour for bug in bugs])

    hours_in_a_day = 24
    hours = [str(i) for i in range(hours_in_a_day)]
    commits = [hours_commits[i] for i in range(hours_in_a_day)]
    bugs = [hours_bugs[i] for i in range(hours_in_a_day)]

    sns.barplot(x=hours, y=commits, label="All commits", palette=PALETTE)
    sns.barplot(x=hours, y=bugs, label="Bug commits", palette=PALETTE)
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3)
    plt.legend()
    plt.show()
