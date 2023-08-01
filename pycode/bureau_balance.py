import pandas as pd
import numpy as np


df = pd.read_csv("../homecredit/bureau_balance.csv")


# df['STATUS'] = df['STATUS'].replace(['C', 'X', '0', '1', '2', '3', '4', '5'], [
#                                     '1', '0', '-1', '-2', '-3', '-4', '-5', '-6']).astype(int)
# ID = df.groupby('ID')
# print(ID.get_group('STATUS'))
# df.to_csv('statusNM.csv')

df = df.groupby("SK_ID_BUREAU")["STATUS"].agg("".join).to_frame()

white = df[df["STATUS"].str.contains(r"^[^a-zA-Z0-9]*[xX]+[^a-zA-Z0-9]*$")]

print(white)

print(white.count(axis=1))


# total = df["STATUS"].count()
# c = df["STATUS"].value_counts()['C']
# print(f'準時繳款:{c}, 占總資料{100*c/total:.2f}%')
# x = df["STATUS"].value_counts()['X']
# print(f'無來往紀錄:{x}, 占總資料{100*x/total:.2f}%')
# thirty = df["STATUS"].value_counts()['0']
# print(f'遲繳1~29天:{thirty}, 占總資料{100*thirty/total:.2f}%')
# sixty = df["STATUS"].value_counts()['1']
# print(f'遲繳30~59天:{sixty}, 占總資料{100*sixty/total:.2f}%')
# ninty = df["STATUS"].value_counts()['2']
# print(f'遲繳60~89天:{ninty}, 占總資料{100*ninty/total:.2f}%')
# onetwenty = df["STATUS"].value_counts()['3']
# print(f'遲繳90~119天:{onetwenty}, 占總資料{100*onetwenty/total:.2f}%')
# onefifty = df["STATUS"].value_counts()['4']
# print(f'遲繳120~149天:{onefifty}, 占總資料{100*onefifty/total:.2f}%')
# baddebts = df["STATUS"].value_counts()['5']
# print(f'遲繳150天以上:{baddebts}, 占總資料{100*baddebts/total:.2f}%')
