from flask import Flask, render_template, request, url_for
from datetime import datetime
from pathlib import Path
import joblib
import xgboost as xgb
import mysql.connector
import plotly.graph_objs as go
import numpy as np
import socket

app = Flask(__name__)

# UPLOAD_FOLDER = (
#     Path(__file__).resolve().parent / "static/uploaded"
# )  # Path(__file__).resolve().parent為此py檔案的父資料夾
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

mysql_config = {
    'host': '172.22.34.127',
    'port': 3306,
    'user': 'wayne',
    'password': 'wayne',
    'database': 'wayne'
}


@app.route("/")
def index():
    return render_template("index.html", page_header="page_header")


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template("form.html", page_header="page_header")
    elif request.method == "POST":
        data = request.form

        form_annual_income = float(request.form['form-annual-income'])

        # 连接到数据库
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # 定义分区条件和标签
        income_ranges = [
            (0, 80000, '5th Zone'),
            (80001, 160000, '4th Zone'),
            (160001, 240000, '3rd Zone'),
            (240001, 320000, '2nd Zone'),
            (320001, float('inf'), '1st Zone')
        ]

        # 根据表单输入查询并标记区间
        income_category = None
        for min_range, max_range, category in income_ranges:
            if min_range <= form_annual_income <= max_range:
                income_category = category
                break

        # 查询数据库以获取区间数据
        cursor.execute("SELECT AMT_INCOME_TOTAL FROM test")
        income_data = [float(row[0]) for row in cursor.fetchall()]

        # 计算每个区间的数量
        income_counts = {}
        for min_range, max_range, _ in income_ranges:
            count = sum(1 for income in income_data if min_range <=
                        income <= max_range)
            income_counts[f"{min_range}-{max_range}"] = count

        # 创建 5 个条形图
        bar_data = []

        for (min_range, max_range, category) in income_ranges:
            # 使用字典的 get 方法，如果键不存在，默认值为 0
            count = income_counts.get(f"{min_range}-{max_range}", 0)

            # 如果 form_annual_income 在当前区间，则设置颜色为橙色
            color = f'rgba(91, 193, 172, 1)' if min_range <= form_annual_income <= max_range else 'rgba(211, 211, 211, 1)'

            # 创建标签文本，根据颜色设置 HTML 样式
            label_text = f'<span style="color:{color};">{category}</span>'

            bar = go.Bar(x=[label_text], y=[
                         count], name=f"{min_range}-{max_range}", marker=dict(color=[color]))
            bar_data.append(bar)

        # 创建布局
        layout = go.Layout(
            title='Income Distribution by Category',
            xaxis=dict(title='Income Range'),
            # yaxis=dict(title='Count'),
            barmode='group',  # 使用 'group' 模式以便并排显示条形图
            showlegend=False,  # 隐藏图例
            # width=400
        )

        # 创建图表
        fig = go.Figure(data=bar_data, layout=layout)

        # 断开数据库连接
        cursor.close()
        connection.close()

        # 将表单数据和图表HTML传递至scoring.html页面
        # return render_template("scoring.html", data=data, plotly_html=plotly_html)

        # 载入模型
        file_name = 'xgb_clf.sav'
        model_path = Path(__file__).resolve().parent / file_name
        model = joblib.load(open(model_path, 'rb'))

        # 构建模型输入数据
        model_input = generate_model_input(data)
        model_input_array = np.array([model_input])

        # 使用模型进行预测
        prediction = model.predict_proba(model_input_array)[0][0]
        # 將預測結果傳遞至 scoring.html
        return render_template("new_scoring.html", data=data, form_annual_income=form_annual_income, income_category=income_category, prediction=prediction, plot=fig.to_html())

        # return render_template("scoring.html", data=data, prediction=prediction, income_category=income_category)


def generate_model_input(data):
    # 在這裡根據映射和表單數據生成模型輸入
    # 将表单数据转换为字典，键为特征名称，值为包含特征值的字典
    mapped_data = {
        'AMT_INCOME_TOTAL': {'value': float(data['form-annual-income'])},
        'CODE_GENDER_M': {'value': 1 if data['form-gender'] == 'male' else 0},
        'CODE_GENDER_XNA': {'value': 0.0 if 'CODE_GENDER_XNA' not in data else float(data['CODE_GENDER_XNA'])},
        'FLAG_OWN_CAR_Y': {'value': 1 if data.get('form-own-car') == 'on' else 0},
        'FLAG_OWN_REALTY_Y': {'value': 1 if data.get('form-own-realty') == 'on' else 0},
        # 其他映射...
    }
    model_input = []

    for feature_data in mapped_data.values():
        model_input.append(feature_data['value'])

    return model_input

# @app.route('/scoring', methods=['POST'])
# def scoring():
#     form_data = request.form.get('form_data')
#     # Parse the form_data string to extract individual field values
#     # ... Process the data as needed
#     return render_template("scoring.html", form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
