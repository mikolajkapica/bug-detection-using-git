import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from typing import Iterable
from collections import Counter


def lines_ratio(
    all_commits: Iterable, bugs: Iterable, maximum_lines: int = None
) -> None:
    if maximum_lines:
        all_commits = [c for c in all_commits if c.insertions < maximum_lines]
        bugs = [bug for bug in bugs if bug.insertions < maximum_lines]

    avg_all_lines, avg_bug_lines = (
        np.mean([c.insertions for c in all_commits]),
        np.mean([bug.insertions for bug in bugs]),
    )

    sns.barplot(x=["All commits", "Bug commits"], y=[avg_all_lines, avg_bug_lines])
    margin = 0.5
    plt.text(0, avg_all_lines + margin, f"{avg_all_lines:.2f} LOC", ha="center")
    plt.text(1, avg_bug_lines + margin, f"{avg_bug_lines:.2f} LOC", ha="center")
    plt.show()


def biggest_commits(all_commits: Iterable, n: int = 10) -> None:
    commits = list(reversed(sorted(all_commits, key=lambda x: x.insertions)))[:n]
    commit_messages = [commit.msg for commit in commits]
    commit_lines = [commit.insertions for commit in commits]

    sns.barplot(x=commit_messages, y=commit_lines)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=-45, ha="left")
    plt.yscale("log")
    plt.show()


def authors_ratio(all_commits: Iterable, bugs: Iterable, n: int = 10) -> None:
    author_commits = Counter([commit.author.name for commit in all_commits])
    author_bugs = Counter([bug.author.name for bug in bugs])

    authors = sorted(author_commits.keys(), key=lambda x: author_commits[x])[::-1][:n]
    commits = [author_commits[author] for author in authors]
    bugs = [author_bugs[author] for author in authors]

    sns.barplot(x=authors, y=commits, label="All commits")
    sns.barplot(x=authors, y=bugs, label="Bug commits")
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

    sns.barplot(x=days, y=commits, label="All commits")
    sns.barplot(x=days, y=bugs, label="Bug commits")
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

    sns.barplot(x=hours, y=commits, label="All commits")
    sns.barplot(x=hours, y=bugs, label="Bug commits")
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3)
    plt.legend()
    plt.show()
