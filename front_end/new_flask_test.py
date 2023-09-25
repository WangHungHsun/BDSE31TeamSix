from flask import Flask, render_template, request, url_for, jsonify, redirect
from pathlib import Path
import joblib
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import socket 

app = Flask(__name__)

# 從CSV檔中載入默認值
csv_data = pd.read_csv('final_cloumns_mode.csv')

# 選擇所有的列除了target
feature_columns = [col for col in csv_data.columns if col not in ['TARGET']]


default_columns = [col for col in csv_data.columns]

# 創建一個包含默認值的字典
default_values = {}
for column in default_columns:
    default_values[column] = csv_data[column].iloc[0]

@app.route("/")
def index():
    return render_template("index.html", page_header="page_header")


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template("form.html", page_header="page_header")
    elif request.method == "POST":
        data = request.form

        df = pd.read_csv('test.csv')

        # 獲取用戶的annual_income
        form_annual_income = float(request.form['form-annual-income'])
        # 獲取用戶的occupation_type
        occupation_type = str(request.form['form-occupation'])
        # 獲取用戶的age
        form_age = int(request.form['form-age'])

        # 定義區間及標籤
        income_ranges = [
            (0, 112500, '4th Zone'),
            (112501, 147150, '3rd Zone'),
            (147151, 202500, '2nd Zone'),
            (202501, float('inf'), '1st Zone')
        ]

        # 根據表單輸入查詢並標記區間
        income_category = None
        for min_range, max_range, category in income_ranges:
            if min_range <= form_annual_income <= max_range:
                income_category = category
                break

        # 獲取 AMT_INCOME_TOTAL 的數據
        income_data = df['AMT_INCOME_TOTAL'].tolist()

        # 計算每個區間的數量
        income_counts = {}
        for min_range, max_range, _ in income_ranges:
            count = sum(1 for income in income_data if min_range <=
                        income <= max_range)
            income_counts[f"{min_range}-{max_range}"] = count

        # 創建長條圖
        bar_data = []

        for (min_range, max_range, category) in income_ranges:
            # 使用字典的 get 方法，如果不存在，默認值為0
            count = income_counts.get(f"{min_range}-{max_range}", 0)

            # 如果 form_annual_income 在當前區間，設置顏色為rgba(91, 193, 172, 1)
            color = f'rgba(91, 193, 172, 1)' if min_range <= form_annual_income <= max_range else 'rgba(211, 211, 211, 1)'

            # 創建標籤文本，根據顏色設置 HTML 樣式
            label_text = f'<span style="color:{color};">{category}</span>'

            bar = go.Bar(x=[label_text], y=[
                         count], name=f"{min_range}-{max_range}", marker=dict(color=[color]))
            bar_data.append(bar)

        # 創建layout
        income_layout = go.Layout(
            title='Income Distribution by Category',
            xaxis=dict(title='Income Range'),
            barmode='group', 
            showlegend=False, 
        )

        # 創建圖表
        fig = go.Figure(data=bar_data, layout=income_layout)

        income_plot_html = fig.to_html()

        # 獲取 OCCUPATION_TYPE 的數據
        occupation_data = df['OCCUPATION_TYPE'].tolist()

        # 計算每種職業類別的數量
        occupation_counts = {}
        for occupation in occupation_data:
            cleaned_occupation = occupation.strip()
            if cleaned_occupation in occupation_counts:
                occupation_counts[cleaned_occupation] += 1
            else:
                occupation_counts[cleaned_occupation] = 1

        # 創建長條圖
        occupation_bar_data = []

        for cleaned_occupation, count in occupation_counts.items():
            # 如果 occupation = 用戶選的 occupation_type，設置顏色為rgba(91, 193, 172, 1)
            color = 'rgba(91, 193, 172, 1)' if cleaned_occupation == occupation_type else 'rgba(211, 211, 211, 1)'

            bar = go.Bar(x=[cleaned_occupation], y=[count],
                         name=cleaned_occupation, marker=dict(color=color))
            occupation_bar_data.append(bar)
        
        
        # 創建layout
        occupation_layout = go.Layout(
            title='Occupation Distribution',
            xaxis=dict(title='Occupation Type', tickvals=list(occupation_counts.keys()), ticktext=list(occupation_counts.keys())),
            barmode='group',
            showlegend=False,
        )

        # 創建職業類別圖表
        occupation_fig = go.Figure(
            data=occupation_bar_data, layout=occupation_layout)

        # 獲取用戶選擇的職業類別
        occupation_type = request.form.get('form-occupation', '')

        # 將圖表命名
        occupation_plot_html = occupation_fig.to_html()

        # 獲取 AGE 的數據
        age_data = df['AGE'].tolist()
        
        # 定義年齡區間和標籤
        age_ranges = [
            (0, 30, 'Under 30'),
            (31, 40, '31-40'),
            (41, 50, '41-50'),
            (51, 60, '51-60'),
            (61, float('inf'), 'Above 60')
        ]

        # 根據表單輸入的年齡查詢並標記區間
        age_category = None
        for min_range, max_range, category in age_ranges:
            if min_range <= form_age <= max_range:
                age_category = category
                break

        # 計算每個年齡層的數量
        age_counts = {}
        for min_range, max_range, _ in age_ranges:
            count = sum(1 for age in age_data if min_range <= age <= max_range)
            age_counts[f"{min_range}-{max_range}"] = count

        # 創建長條圖
        bar_data = []

        for (min_range, max_range, category) in age_ranges:
            # 使用字典的 get 方法，如果不存在，默認值為0
            count = age_counts.get(f"{min_range}-{max_range}", 0)

            # 如果 form_age 在當前區間，設置顏色為rgba(91, 193, 172, 1)
            color = f'rgba(91, 193, 172, 1)' if min_range <= form_age <= max_range else 'rgba(211, 211, 211, 1)'

            # 創建標籤文本，根據顏色設置 HTML 樣式
            label_text = f'<span style="color:{color};">{category}</span>'

            bar = go.Bar(x=[label_text], y=[
                count], name=f"{min_range}-{max_range}", marker=dict(color=[color]))
            bar_data.append(bar)

        # 創建layout
        age_layout = go.Layout(
            title='Age Distribution by Category',
            xaxis=dict(title='Age Range'),
            # yaxis=dict(title='Count'),
            barmode='group',
            showlegend=False, 
            # width=400
        )

        # 創建圖表
        fig = go.Figure(data=bar_data, layout=age_layout)
        # 將圖表命名
        age_plot_html = fig.to_html()
       
        # 定義映射關係
        field_mapping = {
            'form-annual-income': 'AMT_INCOME_TOTAL',
            'form-gender': 'CODE_GENDER_M',
            'CODE_GENDER_XNA': 'CODE_GENDER_XNA',
            'form-own-car': 'FLAG_OWN_CAR_Y',
            'form-own-realty': 'FLAG_OWN_REALTY_Y',
            'form-age':'AGE'
        }


        form_data = dict(request.form)

        # 將默認值加到表單數據
        for column, default_value in default_values.items():
            if column not in form_data:
                form_data[column] = default_value

        # 模型初始值為默認值
        model_input = [float(default_values[column]) for column in feature_columns]

        # 將表單數據映射到模型數據中
        for form_field, model_field in field_mapping.items():
            if form_field in form_data:
                # 表單中有這個填這些選項的話，需要進行類型轉換並更新model_input中的值
                if model_field == 'AMT_INCOME_TOTAL':
                    model_input[feature_columns.index(model_field)] = float(form_data[form_field])
                elif model_field == 'CODE_GENDER_M':
                    model_input[feature_columns.index(model_field)] = 1 if form_data[form_field] == 'male' else 0
                elif model_field == 'CODE_GENDER_XNA':
                    if form_field in form_data:
                        model_input[feature_columns.index(model_field)] = float(form_data[form_field])
                elif model_field == 'FLAG_OWN_CAR_Y':
                    model_input[feature_columns.index(model_field)] = 1 if form_data[form_field] == 'on' else 0
                elif model_field == 'FLAG_OWN_REALTY_Y':
                    model_input[feature_columns.index(model_field)] = 1 if form_data[form_field] == 'on' else 0
                elif model_field == 'AGE':
                    if form_field in form_data:
                        model_input[feature_columns.index(model_field)] = float(form_data[form_field])              
        

        # 創建職業類型到模型字段的映射
        occupation_mapping = {
            'Laborers': 'OCCUPATION_TYPE_Laborers',
            'Sales staff': 'OCCUPATION_TYPE_Salesstaff',
            'Core staff': 'OCCUPATION_TYPE_Corestaff',
            'Managers': 'OCCUPATION_TYPE_Managers',
            'Drivers': 'OCCUPATION_TYPE_Drivers',
            'High skill tech staff': 'OCCUPATION_TYPE_Highskilltechstaff',
            'Medicine staff': 'OCCUPATION_TYPE_Medicinestaff',
            'Security staff': 'OCCUPATION_TYPE_Securitystaff',
            'Cooking staff': 'OCCUPATION_TYPE_Cookingstaff',
            'Cleaning Staff': 'OCCUPATION_TYPE_Cleaningstaff',
            'Private service staff': 'OCCUPATION_TYPE_Privateservicestaff',
            'Low-skill Laborers': 'OCCUPATION_TYPE_LowskillLaborers',
            'Waiters/barmen staff': 'OCCUPATION_TYPE_Waitersbarmenstaff',
            'Secretaries': 'OCCUPATION_TYPE_Secretaries',
            'Realty agents': 'OCCUPATION_TYPE_Realtyagents',
            'HR staff': 'OCCUPATION_TYPE_HRstaff',
            'IT staff': 'OCCUPATION_TYPE_ITstaff',
        }

        # 用戶選擇的職業類型
        selected_occupation = form_data.get('form-occupation')

        # 映射用戶選擇的職業類型到模型字段
        if selected_occupation:
            # 檢查是否存在映射關係
            if selected_occupation in occupation_mapping:
                # 根據用戶選擇的收入類型映射到模型字段，將選擇的職業類型設置為1
                model_field = occupation_mapping[selected_occupation]
                model_input[feature_columns.index(model_field)] = 1
            else:
                # 如果沒有映射關係，補0
                0


        # 創建收入類型到模型字段的映射
        income_type_mapping = {
            'Working': 'NAME_INCOME_TYPE_Working',
            'Commercial Associate': 'NAME_INCOME_TYPE_Commercialassociate',
            'Pensioner': 'NAME_INCOME_TYPE_Pensioner',
            'State Servant': 'NAME_INCOME_TYPE_Stateservant',
            'Unemployed': 'NAME_INCOME_TYPE_Unemployed',
            'Student': 'NAME_INCOME_TYPE_Student',
            'Businessman': 'NAME_INCOME_TYPE_Businessman',
            'Maternity Leave': 'NAME_INCOME_TYPE_Maternityleave',
        }

        # 用戶選擇的收入類型
        selected_income_type = form_data.get('form-income_type')

        # 映射用戶選擇的收入類型到模型字段
        if selected_income_type:
            # 檢查是否存在映射關係
            if selected_income_type in income_type_mapping:
                # 根據用戶選擇的收入類型映射到模型字段，將選擇的收入類型設置為1
                model_field = income_type_mapping[selected_income_type]
                model_input[feature_columns.index(model_field)] = 1
            else:
                # 如果沒有映射關係，補0
                0

        # 創建婚姻類型到模型字段的映射
        family_status_mapping = {
            'married': 'NAME_FAMILY_STATUS_Married',
            'divorced': 'NAME_FAMILY_STATUS_Separated',
            'single': 'NAME_FAMILY_STATUS_Singlenotmarried',
            'unknown': 'NAME_FAMILY_STATUS_Unknown',
            'widowed': 'NAME_FAMILY_STATUS_Widow',
        }

        # 用戶選擇的婚姻類型
        selected_family_type = form_data.get('form-marital-status')

        # 映射用戶選擇的婚姻類型到模型字段
        if selected_family_type:
            # 檢查是否存在映射關係
            if selected_family_type in family_status_mapping:
                # 根據用戶選擇的婚姻類型映射到模型字段，將選擇的婚姻類型設置為1
                model_field = family_status_mapping[selected_family_type]
                model_input[feature_columns.index(model_field)] = 1
            else:
                # 如果沒有映射關係，補0
                0        

        # 創建教育程度到模型字段的映射
        education_type_mapping = {
            'graduate': 'NAME_EDUCATION_TYPE_Highereducation',
            'university': 'NAME_EDUCATION_TYPE_Incompletehigher',
            'high-school': 'NAME_EDUCATION_TYPE_Lowersecondary',
            'college': 'NAME_EDUCATION_TYPE_Secondarysecondaryspecial',
        }

        # 用戶選擇的教育程度
        selected_education_type = form_data.get('form-education-level')

        # 映射用戶選擇的婚姻類型到模型字段
        if selected_education_type:
            # 檢查是否存在映射關係
            if selected_education_type in education_type_mapping:
                # 根據用戶選擇的婚姻類型映射到模型字段，將選擇的婚姻類型設置為1
                model_field = education_type_mapping[selected_education_type]
                model_input[feature_columns.index(model_field)] = 1
            else:
                # 如果沒有映射關係，補0
                0        

        # 載入模型
        file_name = 'LightGBM_v3.sav'
        model_path = Path(__file__).resolve().parent / file_name
        model = joblib.load(open(model_path, 'rb'))

        # 使用模型進行預測
        prediction = model.predict_proba([model_input])[0][0]

        # 將預測結果傳遞至 scoring.html
        return render_template("scoring.html",
                       data=data,
                       form_annual_income=form_annual_income,
                       income_category=income_category,
                       prediction=prediction,
                       income_plot_html=income_plot_html,
                       occupation_plot_html=occupation_plot_html,
                       occupation_type=occupation_type,
                       age_category=age_category,
                       age_plot_html=age_plot_html)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

