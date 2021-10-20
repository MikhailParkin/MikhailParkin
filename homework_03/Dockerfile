# docker run my_app
FROM python:3.9-buster

WORKDIR /var/app

EXPOSE 8000/tcp

#RUN apt update && apt upgrade

CMD python -V

RUN pip install poetry==1.1.11

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install

COPY my_app.py .

CMD uvicorn my_app:app --host=0.0.0.0
