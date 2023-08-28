from flask import Flask, render_template, request, url_for
from datetime import datetime
from pathlib import Path
import uuid
import json
import joblib
import pickle

app = Flask(__name__)

# UPLOAD_FOLDER = (
#     Path(__file__).resolve().parent / "static/uploaded"
# )  # Path(__file__).resolve().parent為此py檔案的父資料夾
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB


@app.route("/")
def index():
    return render_template("index.html", page_header="page_header")





@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
       return render_template("form.html", page_header="page_header")
    elif request.method == "POST":
        data = request.form
        # form_data=[]
        # form_name = data.get('form-name')
        # form_gender = data.get('form-gender')
        # form_age = data.get('form-age')
        # form_marital_status = data.get('form-marital-status')
        # form_education_level = data.get('form-education-level')
        # form_annual_income = data.get('form-annual-income')
        # form_income_type = data.get('form-income_type')
        # form_occupation = data.get('form-occupation')
        # form_own_realty = data.get('form-own-realty')
        # form_own_car = data.get('form-own-car')
        # form_loan_type = data.get('form-loan-type')
        # form_lona_period = data.get('form-lona-period')
        # form_amount_annuity = data.get('form-amount-annuity')
        # form_amount_credit = data.get('form-amount-credit') 

        # 載入模型
        model_path = Path(__file__).resolve().parent / 'xgb_clf.pkl'
        model = pickle.load(open(model_path, 'rb'))

        # 表單欄位名稱到模型特徵名稱的映射
        field_to_feature_mapping = {
            'form-name': 'SK_ID_CURR',
            'form-gender': 'CODE_GENDER',
            'form-own-car': 'FLAG_OWN_CAR',
            'form-own-realty': 'FLAG_OWN_REALTY',
            # 其他映射...
        }

        # 在這裡根據模型需求生成模型特徵
        model_input = generate_model_input(data, field_to_feature_mapping)


        # 使用模型進行預測
        predicted_score = model.predict(model_input)

        # 傳遞表單數據和預測結果至 scoring.html

        return render_template("scoring.html", data=data, predicted_score=predicted_score)
        
        # for key, value in data.items():
        #   form_data += f"{key}: {value}\n"   
        # return render_template("scoring.html", data=data)

    print(data.form_name)
    
@app.route('/scoring', methods=['POST'])
def scoring():
    form_data = request.form.get('form_data')
    # Parse the form_data string to extract individual field values
    # ... Process the data as needed
    return render_template("scoring.html", form_data=form_data)

def generate_model_input(form_data, field_mapping):
    # 在這裡根據映射和表單數據生成模型輸入
    # 需要將表單數據轉換為模型所需的特徵值
    model_input = []

    for model_feature_name in field_mapping.values():
        if model_feature_name in form_data:
            feature_value = form_data[model_feature_name]
            model_input.append(feature_value)
        else:
            # 使用預設值處理缺少的特徵值
            default_value = get_default_value_for_feature(model_feature_name)
            model_input.append(default_value)

    return [model_input]  # 將模型輸入列表轉換為模型所需的格式（例如 Numpy 數組）

# @app.route("/rec", methods=["GET", "POST"])
# def get_file():
#     if request.method == "GET":
#         return render_template("file.html", page_header="upload hand write picture")
#     elif request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = str(uuid.uuid4()) + "_" + file.filename
#             file.save(app.config["UPLOAD_FOLDER"] / filename)
#             predict = model.recog_digit(filename)
#         return render_template(
#             "recog_result.html",
#             page_header="hand writing digit recognition",
#             predict=predict,
#             src=url_for("static", filename=f"uploaded/{filename}"),
#         )
def get_default_value_for_feature(feature_name):
    # 根據特徵名稱返回對應的預設值
    # 這裡可以根據不同特徵名稱返回不同的預設值
    if feature_name == 'AMT_INCOME_TOTAL':
        return 0  # 例如，將收入的缺失值設置為 0
    elif feature_name == 'CODE_GENDER':
        return 'UNKNOWN'  # 例如，將性別的缺失值設置為 'UNKNOWN'
    else:
        return None  # 其他特徵的預設值，根據需求返回適當的值

if __name__ == "__main__":
    app.run(debug=True)
