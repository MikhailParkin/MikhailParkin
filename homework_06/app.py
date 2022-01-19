"""
### Домашнее задание "Взаимодействие между контейнерами"
#### Задача:
- создайте docker-compose файл, настройте там связь базы данных и веб-приложения
- добавьте в свой проект модели. Это могут быть те же модели, что были использованы для сохранения данных с открытого API, это может быть и что-то новое
- добавьте возможность создавать новые записи
- создайте страницу, на которой эти записи выводятся
- база данных должна быть в отдельном контейнере
- Flask приложение должно запускаться не в debug режиме, а в production-ready (uwsgi, nginx, gunicorn)
#### Критерии оценки:
- docker-compose файл присутствует и работает
- приложение взаимодействует с БД
- в приложении есть возможность добавить записи, они сохраняются в БД
- в приложении есть страница, которая выдаёт доступные записи (вытаскивает из БД)
- Flask приложение настроено для запуска в production режиме (uwsgi, nginx, gunicorn)
"""

from flask import Flask, render_template
from flask_migrate import Migrate
from views.table_comp import table_app

from models import db

app = Flask(__name__)
app.register_blueprint(table_app, url_prefix="/table/")

app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://app:password@localhost:5432/blog"
)

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/", endpoint="index")
def root():
    return render_template("index.html")


@app.route("/about/", endpoint="about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)