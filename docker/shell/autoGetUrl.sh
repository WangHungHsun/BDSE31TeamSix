username="Your Name"
mail="youremail@example.com"
#alfred0307/ngroktest0920 -> 替換成你的帳號跟專案名稱
githubUrl="git@github.com:alfred0307/ngroktest0920.git"

sudo cp ~/autoGetUrl/getUrl.service /etc/systemd/system/getUrl.service
cd ~/autoGetUrl/
git config --global user.name $username
git config --global user.email $mail
git init
git remote set-url origin $githubUrl
git add .
git commit -m "更新url"
git push -f origin master
sudo systemctl enable getUrl.service
