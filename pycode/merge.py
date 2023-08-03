import pycaret.classification as clf
from tabulate import tabulate
import pandas as pd
import numpy as np
import time

start_time = time.time()
# pos = pd.read_csv("../../../homecredit/POS_CASH_balance.csv")

# prev = pd.read_csv("../../../homecredit/previous_application.csv")

information = pd.read_csv("../../../homecredit/application_train.csv")
# creditcard = pd.read_csv("../../../homecredit/credit_card_balance.csv")

instalments = pd.read_csv("../../../homecredit/installments_payments.csv")

# print(prev.head(20))
# print(f'客戶與Homecredit申請貸款的歷史資料:{prev.shape}')
# print(pos.head(20))
# print(f'Homecredit的內部資料:{pos.shape}')

# selected_columns = prev.iloc[:, 0:8]
# headers = selected_columns.columns.tolist()
# print(tabulate(selected_columns, headers=headers, tablefmt="pretty"))
# pos = pos[pos["SK_ID_PREV"] == 2154916]

# pos = pos.sort_values(by=["SK_ID_CURR", "SK_ID_PREV", "MONTHS_BALANCE"])
# print(pos.head(10))

# print(tabulate(pos, headers=pos.columns.tolist(), tablefmt="pretty"))
# # creditcard = creditcard[creditcard["SK_ID_PREV"] == 2154916]
# # print(f'creditcard:{creditcard}')
# installments = installments[installments["SK_ID_PREV"] == 2154916]
# instalments = instalments.sort_values(
#     by=["SK_ID_CURR", "SK_ID_PREV", "NUM_INSTALMENT_NUMBER"]
# )
# print(instalments.head())
# print(tabulate(installments, headers=installments.columns.tolist(), tablefmt="pretty"))


# 將實付比應付多的筆數DROP掉
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
information = information[
    [
        "SK_ID_CURR",
        "TARGET",
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
# prev = prev[
#     [
#         "SK_ID_PREV",
#         "SK_ID_CURR",
#         "NAME_CONTRACT_TYPE",
#         "AMT_ANNUITY",
#         "AMT_APPLICATION",
#         "AMT_CREDIT",
#         "AMT_DOWN_PAYMENT",
#         "AMT_GOODS_PRICE",
#         "NAME_CONTRACT_STATUS",
#         "NAME_CLIENT_TYPE",
#         "NAME_PORTFOLIO",
#     ]
# ]
# print(f'實付比應付多的筆數:{countPositive}')
# print(countPositive1.head(50))

# creditcard = creditcard.sort_values(by=["SK_ID_CURR", "SK_ID_PREV", "MONTHS_BALANCE"])
# print(prev.columns)
# print(creditcard.shape)


# # 顯示合併結果
# print(merged_df.head(30))

# 印出合併後的結果
# print(final_df.head(20))

# 記錄程式結束時間
end_time = time.time()

# 計算並印出程式執行時間
execution_time = end_time - start_time
print("程式執行時間:", execution_time, "秒")
