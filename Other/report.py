import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore

import report_gui
import yaml
import mysql.connector


class ParentWindow(QMainWindow, report_gui.Ui_MainWindow):

    username_sql = None
    password_sql = None
    server_sql = None
    day_start = None
    day_end = None
    month_start = None
    month_end = None
    year_start = None
    year_end = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_settings()
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.date_change()
        self.dateEdit.dateChanged.connect(self.date_change)
        self.dateEdit_2.dateChanged.connect(self.date_change)
        self.pushButton.clicked.connect(self.load_report)

    def date_change(self):
        date_start = self.dateEdit.date()
        date_end = self.dateEdit_2.date()
        self.day_start = date_start.day()
        self.month_start = date_start.month()
        self.year_start = date_start.year()
        self.day_end = date_end.day()
        self.month_end = date_end.month()
        self.year_end = date_end.year()

    def load_settings(self):
        with open('settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
        self.username_sql = config.get('username')
        self.password_sql = config.get('password')
        self.server_sql = config.get('server')

    def connect_my_sql(self, command):
        try:
            con = mysql.connector.connect(host=self.server_sql,
                                          user=self.username_sql,
                                          password=self.password_sql,
                                          database="asterisk")
            cur = con.cursor()
            cur.execute(command)
            result = cur.fetchall()
            con.commit()
        except mysql.connector.Error as message:
            print(message)
        return result

    def load_report(self):
        command = f"""
        SELECT accountcode as ls, dst as tel, count(*) as try, 
        case when sum(billsec)  = 0 then 0 else 1 end as answer,
        sum(billsec) as sec, max(summa) as summa
        FROM asterisk.cdr cdr 
        left outer join asterisk.obzvon_number obz on 
        obz.num = cdr.src and obz.lic = cdr.accountcode
        where year(calldate) = {self.year_start}
        and month(calldate) = {self.month_start}
        and day(calldate) >= {self.day_start} 
        and day(calldate) <= {self.day_end}
        group by  accountcode, dst
        order by count(*);
        """
        calls = self.connect_my_sql(command)
        headers = ['Лицевой', 'Номер телефона', 'Попыток', 'Успешных дозвонов', 'Время разговора', 'Сумма задолжности']
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        for row_number, call in enumerate(calls):
            table_item = []
            model.insertRow(row_number)
            for value in call:
                item = QtGui.QStandardItem(str(value))
                table_item.append(item)
            model.insertRow(row_number, table_item)
        self.tableView.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParentWindow()
    window.show()
    app.exec()
