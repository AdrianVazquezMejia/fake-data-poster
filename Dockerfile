#
# Dockerfile
#
FROM python:3.8
WORKDIR /fake-data-poster
COPY main.py .
COPY config.json .
COPY send_later.txt .
COPY sqlite_manager.py .
COPY meter_db.sqlite .
COPY post_http.py .
COPY requirements.txt .
COPY .git .git
ENV TZ=America/Caracas
RUN pip install -r requirements.txt
CMD ["python","main.py"]



