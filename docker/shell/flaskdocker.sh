cd ~/Flask/front_end/
docker build -t flask .
docker run -d --name flask --restart=always -p 8080:8080 flask