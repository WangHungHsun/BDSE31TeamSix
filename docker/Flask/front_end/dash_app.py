import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import mysql.connector

# 创建Dash应用程序
app_dash = dash.Dash(__name__)

# 添加布局
app_dash.layout = html.Div([
    dcc.Graph(id='income-chart'),
    dcc.Graph(id='occupation-chart'),
    dcc.Graph(id='age-chart')
])

# 连接到MySQL数据库
mysql_config = {
    'host': '172.22.34.127',
    'port': 3306,
    'user': 'wayne',
    'password': 'wayne',
    'database': 'wayne'
}

connection = mysql.connector.connect(**mysql_config)
cursor = connection.cursor()

# 定义回调来更新图表
@app_dash.callback(
    Output('income-chart', 'figure'),
    Output('occupation-chart', 'figure'),
    Output('age-chart', 'figure'),
    [Input('income-chart', 'clickData'),
     Input('occupation-chart', 'clickData'),
     Input('age-chart', 'clickData')]
)
def update_charts(income_click_data, occupation_click_data, age_click_data):
    # 在这里根据用户的点击事件更新图表数据
    # 这里示例代码，请根据实际需求更新图表数据

    # 用户点击收入图表
    if income_click_data:
        selected_income_category = income_click_data['points'][0]['x']

        # 使用 selected_income_category 查询相应数据
        cursor.execute("SELECT OCCUPATION_TYPE, AGE_CATEGORY FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
        result = cursor.fetchall()
        if result:
            selected_occupation = result[0][0]
            selected_age_category = result[0][1]

            # 使用选定的职业和年龄区间来查询相应的数据
            # 查询职业图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
            occupation_count = cursor.fetchone()[0]

            # 查询年龄图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
            age_count = cursor.fetchone()[0]

            # 创建职业图表
            occupation_fig = go.Figure()
            occupation_fig.add_trace(go.Bar(x=[selected_occupation], y=[occupation_count], name="Selected Occupation"))
            occupation_fig.update_layout(title='Occupation Distribution', xaxis_title='Occupation Type', showlegend=False)

            # 创建年龄图表
            age_fig = go.Figure()
            age_fig.add_trace(go.Bar(x=[selected_age_category], y=[age_count], name="Selected Age Category"))
            age_fig.update_layout(title='Age Distribution', xaxis_title='Age Category', showlegend=False)


    # 用户点击职业图表
    if occupation_click_data:
        selected_occupation = occupation_click_data['points'][0]['x']

        # 使用 selected_occupation 查询相应数据
        cursor.execute("SELECT AMT_INCOME_TOTAL, AGE_CATEGORY FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
        result = cursor.fetchall()
        if result:
            selected_income_category = result[0][0]
            selected_age_category = result[0][1]

            # 示例：从 MySQL 中查询收入图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
            income_data = [int(row[0]) for row in cursor.fetchall()]

            # 示例：从 MySQL 中查询年龄图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
            age_data = [int(row[0]) for row in cursor.fetchall()]

        # 其他更新图表的代码...

    # 用户点击年龄图表
    if age_click_data:
        selected_age_category = age_click_data['points'][0]['x']

        # 使用 selected_age_category 查询相应数据
        cursor.execute("SELECT OCCUPATION_TYPE, AMT_INCOME_TOTAL FROM test WHERE AGE_CATEGORY = %s", (selected_age_category,))
        result = cursor.fetchall()
        if result:
            selected_occupation = result[0][0]
            selected_income_category = result[0][1]

            # 示例：从 MySQL 中查询职业图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE OCCUPATION_TYPE = %s", (selected_occupation,))
            occupation_data = [int(row[0]) for row in cursor.fetchall()]

            # 示例：从 MySQL 中查询收入图表数据
            cursor.execute("SELECT COUNT(*) FROM test WHERE AMT_INCOME_TOTAL = %s", (selected_income_category,))
            income_data = [int(row[0]) for row in cursor.fetchall()]

    # 更新收入图表
    income_fig = ...  # 更新收入图表的数据

    # 更新职业图表
    occupation_fig = ...  # 更新职业图表的数据

    # 更新年龄图表
    age_fig = ...  # 更新年龄图表的数据

    return income_fig, occupation_fig, age_fig

if __name__ == "__main__":
    app_dash.run_server(debug=True)