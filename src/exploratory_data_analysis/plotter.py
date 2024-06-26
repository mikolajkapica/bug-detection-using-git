from datetime import datetime
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

PALETTE_NAME = "viridis"
YELLOW = "#fde725"
GREEN = "#5ec962"
TEAL = "#21918c"
BLUE = "#3b528b"
PURPLE = "#440154"

sns.set_style("whitegrid")
sns.set_palette(sns.color_palette(PALETTE_NAME))

SIZE_WIDTH = 8
SIZE_HEIGHT = 6


class Plotter:
    normal_commits: pd.DataFrame
    buggy_commits: pd.DataFrame
    location: str
    is_save: bool

    def __init__(
        self,
        normal_commits: pd.DataFrame,
        buggy_commits: pd.DataFrame,
        location: str,
        is_save: bool = False,
    ) -> None:
        self.normal_commits = normal_commits
        self.buggy_commits = buggy_commits
        self.location = location
        self.is_save = is_save

    def save_image(self, plot: plt, name: str) -> None:
        plot.savefig(f"{self.location}/{name}.png")

    def count_commits(self) -> None:
        normal_commits_count = len(self.normal_commits)
        buggy_commits_count = len(self.buggy_commits)

        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        sns.barplot(
            x=["Normal commits", "Buggy commits"],
            y=[normal_commits_count, buggy_commits_count],
            hue=["Normal commits", "Buggy commits"],
            palette=[GREEN, PURPLE],
            ax=ax,
        )

        margin = 0.3
        plt.text(
            0, normal_commits_count + margin, f"{normal_commits_count}", ha="center"
        )
        plt.text(1, buggy_commits_count + margin, f"{buggy_commits_count}", ha="center")
        plt.title("Quantity of normal commits and buggy commits")

        if self.is_save:
            self.save_image(plt, "count_commits")

        plt.show()

    def means_of_lines(self) -> None:
        normal_lines_mean = self.normal_commits["lines"].mean()
        buggy_lines_mean = self.buggy_commits["lines"].mean()

        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        sns.barplot(
            x=["Normal commits", "Buggy commits"],
            y=[normal_lines_mean, buggy_lines_mean],
            hue=["Normal commits", "Buggy commits"],
            palette=[GREEN, PURPLE],
            ax=ax,
        )

        margin = 0.3
        plt.text(
            0, normal_lines_mean + margin, f"{normal_lines_mean:.2f} LOC", ha="center"
        )
        plt.text(
            1, buggy_lines_mean + margin, f"{buggy_lines_mean:.2f} LOC", ha="center"
        )
        plt.title("Mean of lines in normal commits and buggy commits")

        if self.is_save:
            self.save_image(plt, "means_of_lines")
        plt.show()

    def medians_of_lines(self) -> None:
        normal_lines_median = self.normal_commits["lines"].median()
        buggy_lines_median = self.buggy_commits["lines"].median()

        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        sns.barplot(
            x=["Normal commits", "Buggy commits"],
            y=[normal_lines_median, buggy_lines_median],
            hue=["Normal commits", "Buggy commits"],
            palette=[GREEN, PURPLE],
            ax=ax,
        )

        margin = 0.3
        plt.text(
            0,
            normal_lines_median + margin,
            f"{normal_lines_median:.2f} LOC",
            ha="center",
        )
        plt.text(
            1, buggy_lines_median + margin, f"{buggy_lines_median:.2f} LOC", ha="center"
        )
        plt.title("Median of lines in normal commits and buggy commits")

        if self.is_save:
            self.save_image(plt, "medians_of_lines")

        plt.show()

    def biggest_commits(self, n: int = 10, logarithmic: bool = False) -> None:
        all_commits = pd.concat([self.normal_commits, self.buggy_commits])
        biggest_commits = all_commits.nlargest(n, "lines").sort_values("lines")

        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        sns.barplot(
            x="hash",
            y="lines",
            hue="hash",
            data=biggest_commits,
            palette=sns.color_palette(PALETTE_NAME, n_colors=n),
            legend=False,
            ax=ax,
        )

        if logarithmic:
            plt.yscale("log")

        plt.title("Biggest commits")
        plt.ylabel("Lines of code")
        plt.xticks(rotation=-45, ha="left")
        plt.grid(axis="y")
        plt.subplots_adjust(bottom=0.3)

        if self.is_save:
            self.save_image(plt, "biggest_commits")

        plt.show()

    def authors_ratio(self, n: int = 10) -> None:
        xs = (
            pd.concat([self.normal_commits, self.buggy_commits], ignore_index=True)[
                "author_name"
            ]
            .value_counts()
            .nlargest(n)
            .sort_values(ascending=False)
            .index
        )
        ys_buggy = [
            len(self.buggy_commits[self.buggy_commits["author_name"] == x]) for x in xs
        ]
        ys_normal = [
            len(self.normal_commits[self.normal_commits["author_name"] == x])
            for x in xs
        ]

        index = np.arange(len(xs))
        bar_width = 0.35

        plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        plt.bar(
            index,
            ys_normal,
            bar_width,
            label="Normal commits",
            color=GREEN,
        )
        plt.bar(
            index + bar_width,
            ys_buggy,
            bar_width,
            label="Buggy commits",
            color=PURPLE,
        )
        plt.title("Number of Buggy and Normal Commits by the Top 10 Authors")
        plt.ylabel("Quantity of commits")
        plt.xticks(index + bar_width / 2, xs, rotation=-45, ha="left")
        plt.subplots_adjust(bottom=0.2)
        plt.legend()

        if self.is_save:
            self.save_image(plt, "top_authors")

        plt.show()

    def weekday_ratio(self) -> None:
        bar_width = 0.35

        days_normal_commits: Counter[int] = Counter(
            self.normal_commits["author_date"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z").weekday()
            )
        )
        days_buggy_commits: Counter[int] = Counter(
            self.buggy_commits["author_date"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z").weekday()
            )
        )

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        commits = [days_normal_commits[i] for i in range(7)]
        bugs = [days_buggy_commits[i] for i in range(7)]
        indexes = np.arange(len(days))

        plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        plt.bar(
            indexes,
            commits,
            bar_width,
            label="Normal commits",
            color=GREEN,
        )
        plt.bar(
            indexes + bar_width,
            bugs,
            bar_width,
            label="Buggy commits",
            color=PURPLE,
        )

        plt.title("Number of Buggy and Normal Commits by Weekday")
        plt.ylabel("Quantity of commits")
        plt.xticks(rotation=-45, ha="left", ticks=indexes + bar_width / 2, labels=days)
        plt.subplots_adjust(bottom=0.2)
        plt.legend()

        if self.is_save:
            self.save_image(plt, "weekday_ratio")

        plt.show()

    def hour_ratio(self) -> None:
        hours_normal_commits: Counter[int] = Counter(
            self.normal_commits["author_date"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z").hour
            )
        )
        hours_buggy_commits: Counter[int] = Counter(
            self.buggy_commits["author_date"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S%z").hour
            )
        )

        hours = [str(i) for i in range(24)]
        normal_commits = [hours_normal_commits[i] for i in range(24)]
        buggy_commits = [hours_buggy_commits[i] for i in range(24)]
        indexes = np.arange(len(hours))
        bar_width = 0.35

        plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        plt.bar(
            indexes,
            normal_commits,
            bar_width,
            label="Normal commits",
            color=GREEN,
        )
        plt.bar(
            indexes + bar_width,
            buggy_commits,
            bar_width,
            label="Buggy commits",
            color=PURPLE,
        )

        plt.title("Number of Buggy and Normal Commits by Hour")
        plt.ylabel("Quantity of commits")
        plt.xlabel("Hour")
        plt.xticks(ha="center", ticks=indexes + bar_width / 2, labels=hours)
        plt.legend()

        if self.is_save:
            self.save_image(plt, "hour_ratio")

        plt.show()

    def correlation_matrix(self) -> None:
        all_commits = pd.concat([self.normal_commits, self.buggy_commits])
        all_commits.drop(
            ["hash", "msg", "author_name", "author_date", "author_timezone", "merge"],
            axis=1,
            inplace=True,
        )

        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))
        corr = all_commits.corr("pearson")
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(
            corr,
            mask=mask,
            cmap=PALETTE_NAME,
            annot=True,
            fmt=".2f",
            ax=ax,
        )
        ax.grid(False)
        # move everything to the center
        plt.tight_layout()
        plt.subplots_adjust(left=0.2, bottom=0.25, top=0.9)

        plt.title("Correlation matrix")

        if self.is_save:
            self.save_image(plt, "correlation_matrix")

        plt.show()

    def distribution_lines(self) -> None:
        fig, ax = plt.subplots(figsize=(SIZE_WIDTH, SIZE_HEIGHT))

        sns.histplot(
            data=self.normal_commits["lines"],
            label="Normal commits",
            color=GREEN,
            ax=ax,
            kde=True,
        )
        sns.histplot(
            data=self.buggy_commits["lines"],
            label="Buggy commits",
            color=PURPLE,
            ax=ax,
            kde=True,
        )

        plt.title("Distribution of lines of code")
        plt.ylabel("Quantity of commits")
        plt.legend()

        if self.is_save:
            self.save_image(plt, "distribution_lines")

        plt.show()
