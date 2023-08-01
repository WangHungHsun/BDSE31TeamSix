import pandas as pd
import numpy as np

personalTest = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/application_test.csv"
)
print(f"personalTest:{personalTest.shape}")

personalTrain = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/application_train.csv"
)
print(f"personalTrain:{personalTrain.shape}")

bureau = pd.read_csv("D:/期中專題/GitHub/BDSE31TeamSix/homecredit/bureau.csv")
print(f"聯徵紀錄:{bureau.shape}")

bureau_balance = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/bureau_balance.csv"
)
print(f"聯徵紀錄還款狀況:{bureau_balance.shape}")

POS_CASH_balance = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/POS_CASH_balance.csv"
)
print(f"POS_CASH_balance:{POS_CASH_balance.shape}")

installments_payments = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/installments_payments.csv"
)
print(f"installments_payments:{installments_payments.shape}")

previous_application = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/previous_application.csv"
)
print(f"previous_applicatio:{previous_application.shape}")

credit_card_balance = pd.read_csv(
    "D:/期中專題/GitHub/BDSE31TeamSix/homecredit/credit_card_balance.csv"
)
print(f"credit_card_balance:{credit_card_balance.shape}")
