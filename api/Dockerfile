FROM python:3.14-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 41102
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:41102", "app:app"]
