import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore

import report_gui
import yaml
import mysql.connector
import xlsxwriter


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
    calls = None

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
        self.pushButton_2.clicked.connect(lambda: self.save_xlsx(calls=self.calls))
        self.dlg_m = QMessageBox()

    def date_change(self):
        date_start = self.dateEdit.date()
        date_end = self.dateEdit_2.date()
        self.day_start = date_start.day()
        self.month_start = date_start.month()
        self.year_start = date_start.year()
        self.day_end = date_end.day()
        self.month_end = date_end.month()
        self.year_end = date_end.year()

    def alert_message(self, text, message):
        self.dlg_m.show()
        self.dlg_m.setIcon(QMessageBox.Information)
        self.dlg_m.setWindowTitle("Info")
        self.dlg_m.setText(text)
        self.dlg_m.setInformativeText(message)

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
        where calldate >= '{self.year_start}-{self.month_start}-{self.day_start}'
        and calldate <= '{self.year_end}-{self.month_end}-{self.day_end}'
        group by  accountcode, dst
        order by count(*);
        """
        calls = self.connect_my_sql(command)
        headers = ['??????????????', '?????????? ????????????????', '??????????????', '???????????????? ????????????????', '?????????? ??????????????????', '?????????? ??????????????????????']
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
        self.calls = calls

    def save_xlsx(self, calls):

        with xlsxwriter.Workbook(f'??????????{self.year_start}{self.month_start}{self.day_end}.xlsx') as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 18)
            worksheet.set_column('C:C', 10)
            worksheet.set_column('D:D', 18)
            worksheet.set_column('E:E', 18)
            worksheet.set_column('F:F', 18)
            worksheet.write('A1', '??????????????')
            worksheet.write('B1', '?????????? ????????????????')
            worksheet.write('C1', '??????????????')
            worksheet.write('D1', '???????????????? ????????????????')
            worksheet.write('E1', '?????????? ??????????????????')
            worksheet.write('F1', '?????????? ??????????????????????')
            for row_number, call in enumerate(calls):
                for value, values in enumerate(call):
                    worksheet.write(row_number + 1, value, values)
        self.alert_message('', f'???????? ????????????, ?????????????????? {len(calls)} ??????????????')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParentWindow()
    window.show()
    app.exec()
