FROM python:3-buster

COPY ./app /app

WORKDIR /app

RUN pip install wagtail \
    && pip install -r requirements.txt

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
