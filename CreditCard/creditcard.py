import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing


df = pd.read_csv("./credit_record.csv")
x= df["STATUS"].value_counts()['C']
print(x)

