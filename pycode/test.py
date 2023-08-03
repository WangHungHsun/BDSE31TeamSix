import pycaret.classification as clf
from tabulate import tabulate
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz
import os

# os.environ["PATH"] += os.pathsep + 'D:/上課資料/機器學習/實作/hands-on_part5/example/release/bin'


# # Load data
# iris = load_iris()
# X = iris.data
# y = iris.target

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# scaler = preprocessing.StandardScaler().fit(X_train)
# X_train = scaler.transform(X_train)

# model = RandomForestClassifier(max_depth=6, n_estimators=10) #最多10棵樹 每顆最深6個分支
# model.fit(X_train, y_train)

# X_test = scaler.transform(X_test)
# y_pred = model.predict(X_test)


# accuracy = accuracy_score(y_test, y_pred)
# num_correct_samples = accuracy_score(y_test, y_pred, normalize=False)
# con_matrix = confusion_matrix(y_test, y_pred)

# print('number of correct sample: {}'.format(num_correct_samples))
# print('accuracy: {}'.format(accuracy))
# print('con_matrix: {}'.format(con_matrix))

# for i_tree, tree_in_forest in enumerate(model.estimators_):
#     dot_data = tree.export_graphviz(tree_in_forest, out_file = None)
#     graph = graphviz.Source(dot_data)
#     graph.format = 'png'
#     graph.render('./random_forest_plot/tree_' + str(i_tree))
#     #from IPython.display import display, Image
#     #Image(graph.render('output-graph.gv'))
#     #break
# Replace 'iris' with your dataset name or use your own data.
# dataset = pd.read_csv("../../../homecredit/merge.csv")
# clf.setup(data=dataset, target="TARGET")
# best_model = clf.compare_models()
# print(best_model)

start_time = time.time()

instalments = pd.read_csv("../../../homecredit/installments_payments.csv")

instalments = instalments.drop(
    instalments[instalments["AMT_INSTALMENT"] < instalments["AMT_PAYMENT"]].index
).sort_values(by=["SK_ID_CURR", "SK_ID_PREV", "NUM_INSTALMENT_NUMBER"])


# 計算每人平均貸款期數
instalmentsGroup = instalments.groupby("SK_ID_PREV").count()
instalmentsGroup = instalmentsGroup.iloc[:, 1]

count = pd.merge(instalments, instalmentsGroup, on="SK_ID_PREV").sort_values(
    by=["SK_ID_CURR", "SK_ID_PREV", "NUM_INSTALMENT_NUMBER"]
)

count = (
    count[["SK_ID_CURR", "NUM_INSTALMENT_VERSION_y"]]
    .drop_duplicates()
    .groupby("SK_ID_CURR")
    .mean()
    .rename(
        columns={
            "NUM_INSTALMENT_VERSION_y": "Period_Mean",
        }
    )
    .reset_index()
)


information = pd.read_csv("../../../homecredit/application_test.csv")

information = information[
    [
        "SK_ID_CURR",
        "NAME_CONTRACT_TYPE",
        "CODE_GENDER",
        "FLAG_OWN_CAR",
        "FLAG_OWN_REALTY",
        "CNT_CHILDREN",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "NAME_INCOME_TYPE",
        "NAME_EDUCATION_TYPE",
        "NAME_FAMILY_STATUS",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
    ]
]


merge = pd.merge(information, count, on="SK_ID_CURR").sort_values(by=["SK_ID_CURR"])
print(information.head(20))
merge.to_csv("mergetest.csv")
end_time = time.time()

# 計算並印出程式執行時間
execution_time = end_time - start_time
print("程式執行時間:", execution_time, "秒")
