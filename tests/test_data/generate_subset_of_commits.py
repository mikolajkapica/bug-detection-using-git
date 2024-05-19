import numpy as np

if __name__ == "__main__":
    with open("commits.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()
        random_lines = np.random.choice(lines[1:], 100, replace=False)
        with open("commits_sample.csv", "w", encoding="utf-8") as new_file:
            new_file.write(lines[0])
            new_file.writelines(random_lines)
