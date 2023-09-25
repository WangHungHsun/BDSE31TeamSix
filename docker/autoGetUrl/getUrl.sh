#!/bin/bash

#睡三秒 測過這樣才吃得到不然會none
sleep 3

# 切換到git管控的目錄
cd /home/bigred/autoGetUrl/

# 執行 Python 腳本
python3 /home/bigred/autoGetUrl/changeUrl.py

# 添加所有更改到 Git
git add .

# 提交更改
git commit -m "Update URL"

# 推送更改到github（使用 -f 強制推送）
git push -f