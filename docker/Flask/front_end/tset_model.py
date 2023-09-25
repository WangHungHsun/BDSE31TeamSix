from flask import Flask, render_template, request, url_for
from datetime import datetime
from pathlib import Path
import uuid
import json
import joblib
import pickle
import xgboost as xgb
import numpy as np
import pandas as pd

file_name = 'xgb_clf.sav'
# 載入模型
model_path = Path(__file__).resolve().parent / file_name
model = joblib.load(open(model_path, 'rb'))
print(xgb.__version__)

# 表單欄位名稱到模型特徵名稱的映射
field_to_feature_mapping = {
    'AMT_INCOME_TOTAL': [6000000],
    'CODE_GENDER_M': [0],
    'CODE_GENDER_XNA': [0],
    'FLAG_OWN_CAR_Y': [0],
    'FLAG_OWN_REALTY_Y': [0],
    # 其他映射...
}

# 在這裡根據映射和表單數據生成模型輸入
# model_input = generate_model_input(data, field_to_feature_mapping)
model_input = field_to_feature_mapping
model_input_array = pd.DataFrame(model_input)

# 使用模型進行預測
prediction = model.predict_proba(model_input_array)[0][1]
print(prediction)
