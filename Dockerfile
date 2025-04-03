FROM python:3.9.21-slim
WORKDIR /app
COPY app.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
