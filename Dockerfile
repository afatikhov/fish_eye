FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY .env /app/
COPY . /app/

ENV PYTHONPATH=/app/src

EXPOSE 8038

CMD ["python3", "./src/main.py"]