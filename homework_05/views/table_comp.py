from flask import Blueprint, render_template, request, redirect, url_for

table_app = Blueprint("table_app", __name__)


result = [
    {'DN': 'CN=TM-WS9025,OU=Кореновский ПУ,OU=ПК K2 с контролем устройств,OU=Компьютеры,OU=Тимашевск,OU=ТНС_энерго_Кубань,DC=kesk,DC=local - STATUS: Read - READ TIME: 2021-12-06T12:22:10.262983',
    'description': 'Лубенцова Светлана Анатольевна 06.12.2021 8:03:17 Logged on', 'lastLogon': '2018-08-03 10:53:57.966368+00:00', 'name': 'TM-WS9025'},
    {'DN': 'CN=IA-WS3033,OU=2X_FAC_SNS,OU=Компьютеры,OU=Исполнительный аппарат,OU=ТНС_энерго_Кубань,DC=kesk,DC=local - STATUS: Read - READ TIME: 2021-12-06T12:22:10.262983',
    'description': 'Лубашевская Екатерина Игоревна 06.12.2021 9:42:09 Logged on', 'lastLogon': '2021-12-06 06:19:00.721258+00:00', 'name': 'IA-WS3033'}]


@table_app.route("/", endpoint="table")
def table():
    return render_template("table.html", items=result)




