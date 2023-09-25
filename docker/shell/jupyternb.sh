mkdir -p ~/jupyterworkspace/{3.11,3.9,3.10}
docker pull jupyter/scipy-notebook:python-3.11
docker run -d --name j1 --restart=always -p 8888:8888 -v ~/jupyterworkspace/3.11:/home/jovyan/ jupyter/scipy-notebook:python-3.11
docker pull jupyter/scipy-notebook:python-3.9
docker run -d --name j2 --restart=always -p 8889:8888 -v ~/jupyterworkspace/3.9:/home/jovyan/ jupyter/scipy-notebook:python-3.9
docker pull jupyter/scipy-notebook:python-3.10
docker run -d --name j3 --restart=always -p 8890:8888 -v ~/jupyterworkspace/3.10:/home/jovyan/ jupyter/scipy-notebook:python-3.10

#sudo mkdir /jupytertoken;cd /jupytertoken