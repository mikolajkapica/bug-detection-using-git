from dataclasses import dataclass
import pydriller
import graphs

repo = pydriller.Git("C:/Users/mikol/Desktop/vscode")

bug_data = open("../raw_dataset/buggy_hashes_02-05-2024_02-00.txt", "r").readlines()

all_commits = [x for x in (repo.get_list_commits())[:3000] if x.lines > 1000]
bug_commits = [repo.get_commit(bug_commit) for bug_commit in bug_data]
#
# graphs.lines_ratio(all_commits, bug_commits, maximum_lines=1000)
# graphs.biggest_commits(all_commits)
# graphs.authors_ratio(all_commits, bug_commits)
# graphs.days_of_the_week(all_commits, bug_commits)
# graphs.hours_of_the_day(all_commits, bug_commits)
