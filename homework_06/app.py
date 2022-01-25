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
import os

from flask import Flask, render_template, request
from flask_migrate import Migrate

from models import db, add_test_data
from views.author import author_app
from views.posts import post_app

app = Flask(__name__)
app.register_blueprint(author_app, url_prefix="/list/")
app.register_blueprint(post_app, url_prefix="/posts/")

CONFIG_OBJ_PATH = "config.{}".format(os.getenv("CONFIG", "DevelopmentConfig"))
app.config.from_object(CONFIG_OBJ_PATH)

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"], endpoint="index")
def root():
    if request.method == "POST":
        add_test_data()
    return render_template("index.html")


@app.route("/about/", endpoint="about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

