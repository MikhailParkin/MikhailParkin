# docker run -p 8000:8000 my_app
FROM python:3.9-buster

WORKDIR /var/app

#RUN apt update && apt upgrade

CMD python -V

RUN pip install poetry==1.1.11

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install

COPY my_app.py .

CMD uvicorn my_app:app --host=0.0.0.0
