FROM python:latest

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 필요한 패키지를 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



