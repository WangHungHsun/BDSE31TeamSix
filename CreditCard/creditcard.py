import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing


df = pd.read_csv("D:/期中專題/creditcard./credit_record.csv")
print(df.describe)
total = df["STATUS"].count()
c = df["STATUS"].value_counts()['C']
print(f'準時繳款:{c}, 占總資料{100*c/total:.2f}%')
x = df["STATUS"].value_counts()['X']
print(f'無來往紀錄:{x}, 占總資料{100*x/total:.2f}%')
thirty = df["STATUS"].value_counts()['0']
print(f'遲繳1~29天:{thirty}, 占總資料{100*thirty/total:.2f}%')
sixty = df["STATUS"].value_counts()['1']
print(f'遲繳30~59天:{sixty}, 占總資料{100*sixty/total:.2f}%')
ninty = df["STATUS"].value_counts()['2']
print(f'遲繳60~89天:{ninty}, 占總資料{100*ninty/total:.2f}%')
onetwenty = df["STATUS"].value_counts()['3']
print(f'遲繳90~119天:{onetwenty}, 占總資料{100*onetwenty/total:.2f}%')
onefifty = df["STATUS"].value_counts()['4']
print(f'遲繳120~149天:{onefifty}, 占總資料{100*onefifty/total:.2f}%')
baddebts= df["STATUS"].value_counts()['5']
print(f'遲繳150天以上:{baddebts}, 占總資料{100*baddebts/total:.2f}%')

