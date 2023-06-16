FROM python:3.9.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./main.py /app/main.py
COPY ./api /app/api
COPY ./core /app/core
COPY ./db /app/db
COPY ./utils /app/utils

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "main.py"]