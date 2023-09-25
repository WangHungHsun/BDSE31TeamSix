from flask import Flask, render_template, request, url_for, jsonify
from pathlib import Path
import joblib
import mysql.connector
import plotly.graph_objs as go
import numpy as np
import socket
import pandas as pd

app = Flask(__name__)

mysql_config = {
    'host': '172.22.34.127',
    'port': 3306,
    'user': 'wayne',
    'password': 'wayne',
    'database': 'wayne',
    'auth_plugin': "mysql_native_password"
}

# 从CSV文件中加载默认值列
csv_data = pd.read_csv('final_cloumns_mode.csv')

# 选择希望用作默认值的列
feature_columns = [col for col in csv_data.columns if col not in ['TARGET']]

# 这里假设您希望使用所有列（除了SK_ID_CURR和TARGET列）作为默认列
# 您可以根据需要调整选择的列
default_columns = [col for col in csv_data.columns]

# 创建一个包含默认值的字典
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

        form_annual_income = float(request.form['form-annual-income'])
        # 獲取用戶選擇的occupation_type
        occupation_type = str(request.form['form-occupation'])
        # 获取用户在表单中输入的年龄
        form_age = int(request.form['form-age'])

        # 连接到数据库
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # 定义分区条件和标签
        income_ranges = [
            (0, 112500, '4th Zone'),
            (112501, 147150, '3rd Zone'),
            (147151, 202500, '2nd Zone'),
            (202501, float('inf'), '1st Zone')
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
        income_layout = go.Layout(
            title='Income Distribution by Category',
            xaxis=dict(title='Income Range'),
            # yaxis=dict(title='Count'),
            barmode='group',  # 使用 'group' 模式以便并排显示条形图
            showlegend=False,  # 隐藏图例
            # width=400
        )

        # 创建图表
        fig = go.Figure(data=bar_data, layout=income_layout)

        income_plot_html = fig.to_html()

        # 查询数据库以获取职业类型数据
        cursor.execute("SELECT OCCUPATION_TYPE FROM test")
        occupation_data = [row[0] for row in cursor.fetchall()]

        # 计算每种职业类型的数量
        occupation_counts = {}
        for occupation in occupation_data:
            cleaned_occupation = occupation.strip()
            if cleaned_occupation in occupation_counts:
                occupation_counts[cleaned_occupation] += 1
            else:
                occupation_counts[cleaned_occupation] = 1

        # 创建职业类型条形图
        occupation_bar_data = []

        for cleaned_occupation, count in occupation_counts.items():
            # 如果 occupation 等于用户选择的 occupation_type，则设置颜色为青绿色，否则为淡灰色
            color = 'rgba(91, 193, 172, 1)' if cleaned_occupation == occupation_type else 'rgba(211, 211, 211, 1)'

            bar = go.Bar(x=[cleaned_occupation], y=[count],
                         name=cleaned_occupation, marker=dict(color=color))
            occupation_bar_data.append(bar)
        
        
        # 创建布局
        occupation_layout = go.Layout(
            title='Occupation Distribution',
            xaxis=dict(title='Occupation Type', tickvals=list(occupation_counts.keys()), ticktext=list(occupation_counts.keys())),
            barmode='group',  # 使用 'group' 模式以便并排显示条形图
            showlegend=False,  # 隐藏图例
        )

        # 创建职业类型图表
        occupation_fig = go.Figure(
            data=occupation_bar_data, layout=occupation_layout)

        # 在视图函数中获取用户选择的职业类型
        occupation_type = request.form.get('form-occupation', '')

        # 将第二个图表的HTML代码传递给模板
        occupation_plot_html = occupation_fig.to_html()

        # 查询数据库以获取年龄数据
        cursor.execute("SELECT AGE FROM test")
        age_data = [int(row[0]) for row in cursor.fetchall()]

        # 定义年龄区间条件和标签
        age_ranges = [
            (0, 30, 'Under 30'),
            (31, 40, '31-40'),
            (41, 50, '41-50'),
            (51, 60, '51-60'),
            (61, float('inf'), 'Above 60')
        ]

        # 根据表单输入的年龄查询并标记区间
        age_category = None
        for min_range, max_range, category in age_ranges:
            if min_range <= form_age <= max_range:
                age_category = category
                break

        # 查询数据库以获取年龄数据
        cursor.execute("SELECT AGE FROM test")
        age_data = [int(row[0]) for row in cursor.fetchall()]

        # 计算每个年龄区间的数量
        age_counts = {}
        for min_range, max_range, _ in age_ranges:
            count = sum(1 for age in age_data if min_range <= age <= max_range)
            age_counts[f"{min_range}-{max_range}"] = count

        # 创建 5 个条形图
        bar_data = []

        for (min_range, max_range, category) in age_ranges:
            # 使用字典的 get 方法，如果键不存在，默认值为 0
            count = age_counts.get(f"{min_range}-{max_range}", 0)

            # 如果 form_age 在当前区间，则设置颜色为橙色
            color = f'rgba(91, 193, 172, 1)' if min_range <= form_age <= max_range else 'rgba(211, 211, 211, 1)'

            # 创建标签文本，根据颜色设置 HTML 样式
            label_text = f'<span style="color:{color};">{category}</span>'

            bar = go.Bar(x=[label_text], y=[
                count], name=f"{min_range}-{max_range}", marker=dict(color=[color]))
            bar_data.append(bar)

        # 创建布局
        age_layout = go.Layout(
            title='Age Distribution by Category',
            xaxis=dict(title='Age Range'),
            # yaxis=dict(title='Count'),
            barmode='group',  # 使用 'group' 模式以便并排显示条形图
            showlegend=False,  # 隐藏图例
            # width=400
        )

        # 创建图表
        fig = go.Figure(data=bar_data, layout=age_layout)
        # 将图表转换为HTML代码
        age_plot_html = fig.to_html()
    
        # def update_charts(income_click_data, occupation_click_data, age_click_data):
        #     # 在这里根据用户的点击事件更新图表数据
        #     # 这里示例代码，请根据实际需求更新图表数据

        #     # 用户点击收入图表
        #     if income_click_data:
        #         selected_income_category = income_click_data['points'][0]['x']

        #         # 使用 selected_income_category 查询相应数据
        #         cursor.execute("SELECT OCCUPATION_TYPE, AGE_CATEGORY FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
        #         result = cursor.fetchall()
        #         if result:
        #             selected_occupation = result[0][0]
        #             selected_age_category = result[0][1]

        #             # 使用选定的职业和年龄区间来查询相应的数据
        #             # 查询职业图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
        #             occupation_count = cursor.fetchone()[0]

        #             # 查询年龄图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
        #             age_count = cursor.fetchone()[0]

        #             # 创建职业图表
        #             occupation_fig = go.Figure()
        #             occupation_fig.add_trace(go.Bar(x=[selected_occupation], y=[occupation_count], name="Selected Occupation"))
        #             occupation_fig.update_layout(title='Occupation Distribution', xaxis_title='Occupation Type', showlegend=False)

        #             # 创建年龄图表
        #             age_fig = go.Figure()
        #             age_fig.add_trace(go.Bar(x=[selected_age_category], y=[age_count], name="Selected Age Category"))
        #             age_fig.update_layout(title='Age Distribution', xaxis_title='Age Category', showlegend=False)


        #     # 用户点击职业图表
        #     if occupation_click_data:
        #         selected_occupation = occupation_click_data['points'][0]['x']

        #         # 使用 selected_occupation 查询相应数据
        #         cursor.execute("SELECT AMT_INCOME_TOTAL, AGE_CATEGORY FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
        #         result = cursor.fetchall()
        #         if result:
        #             selected_income_category = result[0][0]
        #             selected_age_category = result[0][1]

        #             # 示例：从 MySQL 中查询收入图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
        #             income_data = [int(row[0]) for row in cursor.fetchall()]

        #             # 示例：从 MySQL 中查询年龄图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
        #             age_data = [int(row[0]) for row in cursor.fetchall()]

        #             # 创建年收图表
        #             income_fig = go.Figure()
        #             income_fig.add_trace(go.Bar(x=[selected_income_category], y=[income_counts], name="Selected Income Category"))
        #             income_fig.update_layout(title='Income Distribution', xaxis_title='Income Type', showlegend=False)

        #             # 创建年龄图表
        #             age_fig = go.Figure()
        #             age_fig.add_trace(go.Bar(x=[selected_age_category], y=[age_count], name="Selected Age Category"))
        #             age_fig.update_layout(title='Age Distribution', xaxis_title='Age Category', showlegend=False)

        #             # 创建职业图表
        #             occupation_fig = go.Figure()
        #             occupation_fig.add_trace(go.Bar(x=[selected_occupation], y=[occupation_count], name="Selected Occupation"))
        #             occupation_fig.update_layout(title='Occupation Distribution', xaxis_title='Occupation Type', showlegend=False)

        #     # 用户点击年龄图表
        #     if age_click_data:
        #         selected_age_category = age_click_data['points'][0]['x']

        #         # 使用 selected_age_category 查询相应数据
        #         cursor.execute("SELECT OCCUPATION_TYPE, AMT_INCOME_TOTAL FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
        #         result = cursor.fetchall()
        #         if result:
        #             selected_occupation = result[0][0]
        #             selected_income_category = result[0][1]

        #             # 示例：从 MySQL 中查询职业图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
        #             occupation_data = [int(row[0]) for row in cursor.fetchall()]

        #             # 示例：从 MySQL 中查询收入图表数据
        #             cursor.execute("SELECT COUNT(*) FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
        #             income_data = [int(row[0]) for row in cursor.fetchall()]

        #             # 创建年收图表
        #             income_fig = go.Figure()
        #             income_fig.add_trace(go.Bar(x=[selected_income_category], y=[income_counts], name="Selected Income Category"))
        #             income_fig.update_layout(title='Income Distribution', xaxis_title='Income Type', showlegend=False)

        #             # 构建图表数据和布局
        #     income_chart_data = {
        #         'data': income_data,
        #         'layout': income_layout
        #     }

        #     occupation_chart_data = {
        #         'data': occupation_data,
        #         'layout': occupation_layout
        #     }

        #     age_chart_data = {
        #         'data': age_data,
        #         'layout': age_layout
        #     }

        #     # 返回数据，可以是一个 JSON 对象
        #     response_data = {
        #         'income_chart_data': income_chart_data,
        #         'occupation_chart_data': occupation_chart_data,
        #         'age_chart_data': age_chart_data
        #     }

        #     return jsonify(response_data)


            

            # return income_fig, occupation_fig, age_fig

        # 断开数据库连接
        cursor.close()
        connection.close()
        
        # 定义字段名称的映射关系
        field_mapping = {
            'form-annual-income': 'AMT_INCOME_TOTAL',
            'form-gender': 'CODE_GENDER_M',
            'CODE_GENDER_XNA': 'CODE_GENDER_XNA',  # 没有映射关系，因为字段名相同
            'form-own-car': 'FLAG_OWN_CAR_Y',
            'form-own-realty': 'FLAG_OWN_REALTY_Y',
            'form-age':'AGE'
        }


        form_data = dict(request.form)

        # 将默认值添加到表单数据中
        for column, default_value in default_values.items():
            if column not in form_data:
                form_data[column] = default_value

        # 构建模型输入数据，初始值为默认值
        model_input = [float(default_values[column]) for column in feature_columns]

        # 遍历字段映射关系，将表单数据映射到模型数据中
        for form_field, model_field in field_mapping.items():
            if form_field in form_data:
                # 如果表单中有这个字段，根据需要进行类型转换并更新model_input中的值
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
                    
                # 添加其他字段的处理方式...
        

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

        # 载入模型
        file_name = 'LightGBM_v3.sav'
        model_path = Path(__file__).resolve().parent / file_name
        model = joblib.load(open(model_path, 'rb'))

        # 使用模型进行预测
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
