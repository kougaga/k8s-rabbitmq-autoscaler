FROM python:3.6-alpine

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ${PWD}/queue.py /app/queue.py
COPY ${PWD}/config.ini /app/config.ini

ENTRYPOINT ["python", "queue.py", "consume"]
CMD ["DEFAULT-QUEUE"]
