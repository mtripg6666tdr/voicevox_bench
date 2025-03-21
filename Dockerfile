FROM python:3.13-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bench.py"]
