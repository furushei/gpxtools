FROM python:3.14-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 41101
CMD ["streamlit", "run", "app.py", "--server.port", "41101", "--server.address", "0.0.0.0"]
