import pydriller
import graphs

GIT_REPO_PATH = "C:/Users/mikol/Desktop/vscode"
BUGS_DATASET_PATH = "../dataset/bugs_01-05-2024_20-00.txt"

repo = pydriller.Git(GIT_REPO_PATH)
bugs_dataset = open(BUGS_DATASET_PATH, "r")

all_commits = repo.get_list_commits()
bug_commits = [repo.get_commit(bug_commit) for bug_commit in bugs_dataset.readlines()]

graphs.lines_ratio(all_commits, bug_commits, maximum_lines=1000)
graphs.biggest_commits(all_commits)
graphs.authors_ratio(all_commits, bug_commits)
graphs.days_of_the_week(all_commits, bug_commits)
graphs.hours_of_the_day(all_commits, bug_commits)
