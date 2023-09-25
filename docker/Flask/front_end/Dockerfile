FROM python:3.10-slim
LABEL maintainer="dimon000091@gmail.com"
RUN apt-get update && \
apt-get -y --no-install-recommends install \
libgomp1 nano git 
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir numpy pandas Flask scikit-learn mysql.connector joblib pathlib plotly lightgbm
WORKDIR /app
COPY . /app
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["flask_test.py"]
