#將getUrl.sh放到家目錄

    #如果是要登入之後再更改是nano ~/.bashrc
最後一行添加source ~/getUrl.sh



    #如果是要系統run跟著run
sudo nano /etc/systemd/system/getUrl.service

#省略*** 將包在裡面的code複製貼上
#User=替換成你的使用者
#Group=替換成你的群組

***
[Unit]
Description=Run getUrl.sh at startup
After=docker.service

[Service]
Type=oneshot
ExecStart=/bin/bash /home/bigred/getUrl.sh
User=bigred
Group=bigred

[Install]
WantedBy=multi-user.target
***

#啟動這個自動getUrl的服務
sudo systemctl enable getUrl.service
#現在啟動getUrl的服務
sudo systemctl start getUrl.service

#假設有更改要更新
systemctl daemon-reload
#檢查log
sudo systemctl status getUrl.service