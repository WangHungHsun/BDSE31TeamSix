@echo off
REM 先更新
ssh bigred@172.22.34.129 sudo apt update;sudo apt upgrade -y

REM 重啟
ssh bigred@172.22.34.129 sudo reboot

REM 等開機45s
echo "等開機"
timeout /t 45

REM 提醒有沒有將資料夾做放如
echo "提醒您有無將docker資料夾放到桌面且沒有改名字"

REM 給15秒確認
timeout /t 15

REM 切到資料夾
cd C:\Users\User\Desktop\docker

REM cp image相依檔
scp -r {autoGetUrl,Flask,} bigred@172.22.34.129:~/

REM cp shell
scp -r shell bigred@172.22.34.129:~/

REM 在遠程機器上執行所有的docker build 跟 docker run 命令
ssh bigred@172.22.34.129 ~/shell/docker.sh

REM 在遠程機器上執行autoGetUrl docker build 跟 docker run 命令
ssh bigred@172.22.34.129 ./autoGetUrl.sh

REM
echo "部屬完成"
pause

REM 關閉SSH連接（如果需要）
REM ssh bigred@172.22.34.129 exit
REM 關閉虛擬機（如果需要）
REM "C:\Program Files (x86)\VMware\VMware Player\vmrun" stop C:\DT\a3.129\Iac.vmx
