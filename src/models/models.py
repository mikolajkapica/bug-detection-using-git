from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

type Model = DecisionTreeClassifier | RandomForestClassifier | SVC | LogisticRegression
models = [DecisionTreeClassifier, RandomForestClassifier, SVC, LogisticRegression]
