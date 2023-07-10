import pandas as pd
import numpy as np

oringinalDf = pd.read_csv("BDSE31TeamSix\CreditCard\personalData.csv")
df = oringinalDf.rename(columns={'CODE_GENDER':'GENDER','FLAG_OWN_CAR':'OWNCAR','FLAG_OWN_REALTY':'REALTY','CNT_CHILDREN':'CHILDREN',
'AMT_INCOME_TOTAL':'INCOME','NAME_INCOME_TYPE':'INCOME_TYPE','NAME_EDUCATION_TYPE':'EDUCATION','NAME_FAMILY_STATUS':'FAMILY_STATUS',
'NAME_HOUSING_TYPE':'HOUSING_TYPE','OCCUPATION_TYPE':'JOB','CNT_FAM_MEMBERS':'FAMILY_MEMBERS'})

#change DAYS_BIRTH to AGE
df['DAYS_BIRTH']=df['DAYS_BIRTH']/ 365
df['DAYS_BIRTH'] =df['DAYS_BIRTH'].astype(int).abs()
df = df.rename(columns={'DAYS_BIRTH':'AGE'})

#change DAYS_EMPLOYED to JOB_TENURE
df['DAYS_EMPLOYED']=df['DAYS_EMPLOYED']/ 365
df['DAYS_EMPLOYED'] =df['DAYS_EMPLOYED'].round(1).abs()
df = df.rename(columns={'DAYS_EMPLOYED':'JOB_TENURE'})

df = df.drop(columns=['FLAG_MOBIL','FLAG_WORK_PHONE','FLAG_PHONE','FLAG_EMAIL'])


for col in df.columns:
    print(col)
print(df['JOB'].value_counts())
print(df.columns)
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
# baddebts= df["STATUS"].value_counts()['5']
# print(f'遲繳150天以上:{baddebts}, 占總資料{100*baddebts/total:.2f}%')

