@echo off
REM 移動資料夾
cd C:\Users\User\Desktop\docker

REM 檢查資料夾存不存在，不存在建立，存在則忽略此命令
setlocal
set folderName=DT

REM 檢查資料夾是否存在
if not exist "%folderName%" (
  mkdir "%folderName%"
  echo Folder "%folderName%" created.
) else (
  echo Folder "%folderName%" already exists.
)
endlocal

REM 複製虛擬機
xcopy a3.129 C:\DT\ /s /e

REM 刪除原目錄的a3
rd /s /q a3.129

REM 啟動虛擬機
"C:\Program Files (x86)\VMware\VMware Player\vmrun" start C:\DT\a3.129\Iac.vmx