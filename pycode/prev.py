# for classification tasks, change to .regression for regression tasks
import pycaret.classification as clf
from pycaret.datasets import get_data
from tabulate import tabulate

# Load a classification dataset as an example
# Replace 'iris' with your dataset name or use your own data.
# dataset = get_data('iris')
# clf.setup(data=dataset, target='species')
# best_model = clf.compare_models()
# print(best_model)


import pandas as pd
import numpy as np


pos = pd.read_csv("POS_CASH_balance.csv")

prev = pd.read_csv("previous_application.csv")

creditcard = pd.read_csv("credit_card_balance.csv")

installments = pd.read_csv("installments_payments.csv")


# print(prev.head())
# print(f'客戶與Homecredit申請貸款的歷史資料:{prev.shape}')
# print(pos.head())
# print(f'Homecredit的內部資料:{pos.shape}')
prev = prev[prev["SK_ID_PREV"] == 2154916]
selected_columns = prev.iloc[:, 0:8]
headers = selected_columns.columns.tolist()
print(tabulate(selected_columns, headers=headers, tablefmt="pretty"))
pos = pos[pos["SK_ID_PREV"] == 2154916]
pos = pos.sort_values(by="MONTHS_BALANCE")
print(tabulate(pos, headers=pos.columns.tolist(), tablefmt="pretty"))
# creditcard = creditcard[creditcard["SK_ID_PREV"] == 2154916]
# print(f'creditcard:{creditcard}')
installments = installments[installments["SK_ID_PREV"] == 2154916]
installments = installments.sort_values(by="NUM_INSTALMENT_NUMBER")
print(tabulate(installments, headers=installments.columns.tolist(), tablefmt="pretty"))

# print(pos["NAME_CONTRACT_STATUS"].value_counts())
# groupbySKIDPREV = installments.groupby(['SK_ID_PREV'])
# group_sum = groupbySKIDPREV.get_group(2154916)['AMT_PAYMENT'].sum()
# print(group_sum)
# print(creditcard.head())
# print(f'客戶與Homecredit信用卡的歷史資料:{creditcard.shape}')
# print(installments.head())
# print(f'客戶與Homecredit分期付款的資料:{installments.shape}')
# print(bureau['NAME_CONTRACT_TYPE'].value_counts())
# print(POS.head())
# print(prev.head())
# print(prev.loc[prev['SK_ID_PREV']] == '1803195')
