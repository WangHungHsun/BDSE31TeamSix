import mysql.connector

# 配置MySQL连接参数
mysql_config = {
    'host': '172.22.34.127',
    'port': 3306,
    'user': 'wayne',
    'password': 'wayne',
    'database': 'wayne'
}

try:
    # 连接到MySQL数据库
    connection = mysql.connector.connect(**mysql_config)

    if connection.is_connected():
        print("Connected to MySQL database")

        # 创建游标
        cursor = connection.cursor()

        # 执行查询
        cursor.execute("SELECT * FROM trans")

        # 获取查询结果
        result = cursor.fetchall()

        for row in result:
            print(row)

        # 关闭游标和连接
        cursor.close()
        connection.close()

except mysql.connector.Error as e:
    print("Error:", e)
