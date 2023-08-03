import pycaret.classification as clf
from tabulate import tabulate
import pandas as pd
import numpy as np
import time

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

print(information.head(20))
