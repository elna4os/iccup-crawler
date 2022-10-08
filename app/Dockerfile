FROM python:3.7
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
COPY src/ src/
COPY app.py ./
CMD uvicorn app:APP --host 0.0.0.0