import os
import sys
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from ldap3 import Connection, AUTO_BIND_NO_TLS, SUBTREE

import dlg
import gui
import threading
import re
import yaml


class ParentWindow(QMainWindow, gui.Ui_MainWindow):
    ldap_url = '1.1.1.1'
    username = 'username'
    password = 'password'
    search_base = 'DC=kesk,DC=local'

    def load_settings(self):
        if os.path.exists('settings.yaml') is not True:
            config = {'username': self.username, 'ldap_url': self.ldap_url, 'password': self.password,
                      'search_base': self.search_base}
            print(config)
            with open('settings.yaml', 'w') as f:
                yaml.dump(config, f)
            self.edit_settings()

        with open('settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
        self.username = config.get('username')
        self.ldap_url = config.get('ldap_url')
        self.password = config.get('password')
        self.search_base = config.get('search_base')
        return config

    def search_domain(self, my_comp):

        if len(my_comp) < 1:
            self.empty_line()
            return

        search_filter = '(&(objectClass=computer)(description=*' + my_comp + '*))'
        attributes = ['description', 'lastLogon', 'name']
        entries = ParentWindow.ldap_conn(self, search_filter, attributes)
        row_count = len(entries)
        table = self.tableWidget
        table.setColumnCount(2)
        table.setRowCount(row_count)
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        table.setHorizontalHeaderItem(1, item)
        item = table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Computer"))
        item = table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        table.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        table.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        for row in range(row_count):
            a = str(entries[row]['description'])
            b = str(entries[row]['name'])
            for i in range(1):
                table.setItem(row, i, QtWidgets.QTableWidgetItem(b))
                table.setItem(row, i + 1, QtWidgets.QTableWidgetItem(a))
                table.resizeColumnsToContents()
        print(entries)


    def search_phone(self, my_user):

        def create_table(a, b, c, d):
            table = self.tableWidget_3
            table.setRowCount(row_count)
            table.setColumnCount(4)
            _translate = QtCore.QCoreApplication.translate
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setHorizontalHeaderItem(3, item)
            item = table.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "ФИО"))
            item = table.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Телефон"))
            item = table.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Отдел"))
            item = table.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Должность"))

            table.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
            table.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
            table.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
            table.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignLeft)
            table.setItem(row, i, QtWidgets.QTableWidgetItem(a))
            table.setItem(row, i + 1, QtWidgets.QTableWidgetItem(b))
            table.setItem(row, i + 2, QtWidgets.QTableWidgetItem(c))
            table.setItem(row, i + 3, QtWidgets.QTableWidgetItem(d))
            table.resizeColumnsToContents()
            print(a, b, c, d, row_count)

        if len(my_user) < 1:
            self.empty_line()

        else:
            search_filter = '(&(objectClass=person)(displayName=*' + my_user + '*))'
            attributes = ['displayName', 'telephoneNumber', 'userAccountControl', 'company', 'department',
                          'title']
            entries = ParentWindow.ldap_conn(self, search_filter, attributes)
            row_count = len(entries)
            if row_count > 1:

                for row in range(row_count):
                    acc_state = str(entries[row]['userAccountControl'])
                    tel_empty = str(entries[row]['telephoneNumber'])
                    if acc_state != '514' and len(tel_empty) > 2:
                        a = str(entries[row]['displayName'])
                        b = str(entries[row]['telephoneNumber'])
                        c = str(entries[row]['department'])
                        d = str(entries[row]['title'])
                        for i in range(1):
                            create_table(a, b, c, d)

                    elif acc_state != '514' and len(tel_empty) <= 2:
                        a = str(entries[row]['displayName'])
                        b = str('Номер не указан')
                        c = str(entries[row]['department'])
                        d = str(entries[row]['title'])
                        for i in range(1):
                            create_table(a, b, c, d)
                    elif acc_state == '514':
                        a = str(entries[row]['displayName'])
                        b = str('Номер не указан')
                        c = str('Больше не работает')
                        d = str(entries[row]['title'])
                        for i in range(1):
                            create_table(a, b, c, d)

            if row_count == 1:

                for row in range(row_count):
                    acc_state = str(entries[row]['userAccountControl'])
                    tel_empty = str(entries[row]['telephoneNumber'])
                    if acc_state != '514' and len(tel_empty) > 2:
                        a = str(entries[row]['displayName'])
                        b = str(entries[row]['telephoneNumber'])
                        c = str(entries[row]['department'])
                        d = str(entries[row]['title'])
                        for i in range(1):
                            create_table(a, b, c, d)

                    elif acc_state != '514' and len(tel_empty) <= 2:
                        a = str(entries[row]['displayName'])
                        b = str('Номер не указан')
                        c = str(entries[row]['department'])
                        d = str(entries[row]['title'])
                        for i in range(1):
                            create_table(a, b, c, d)

                    else:
                        self.tableWidget_3.setColumnCount(1)
                        self.tableWidget_3.setItem(0, 0, QtWidgets.QTableWidgetItem('Такой пользователь не найден'))
                        self.tableWidget_3.resizeColumnsToContents()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.text()
        self.dlg = QDialog()
        self.dlg.setWindowTitle("Loading")
        self.dlg.setWindowModality(False)
        self.dlg.setFixedSize(300, 270)
        self.dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.label = QtWidgets.QLabel(self.dlg)
        self.label.setGeometry(-50, -40, 350, 350)
        self.child_window = ChildWindow()
        self.pushButton.clicked.connect(lambda: self.search_domain(my_comp=self.lineEdit.text()))
        self.pushButton_2.clicked.connect(self.select_comp)
        self.pushButton.setAutoDefault(True)
        self.lineEdit.returnPressed.connect(self.pushButton.click)
        self.lineEdit_3.text()
        self.pushButton_7.clicked.connect(lambda: self.search_phone(my_user=self.lineEdit_3.text()))
        self.pushButton.setAutoDefault(True)
        self.lineEdit_3.returnPressed.connect(self.pushButton_7.click)
        self.pushButton_excel.clicked.connect(self.kill_excel)
        self.pushButton_word.clicked.connect(self.kill_word)
        self.pushButton_disk.clicked.connect(self.disc_c)
        self.lineEdit.setFocus()
        self.load_settings()
        self.actionExit.triggered.connect(qApp.quit)
        self.actionSettings.triggered.connect(self.edit_settings)
        self.movie = QtGui.QMovie("loading-52.gif")

    def ldap_conn(self, search_filter, attributes):
        conn = Connection(self.ldap_url, auto_bind=AUTO_BIND_NO_TLS, user=self.username, password=self.password)
        conn.search(search_base=self.search_base,
                    search_filter=search_filter,
                    search_scope=SUBTREE,
                    attributes=attributes,
                    size_limit=0)
        return conn.entries

    def empty_line(self):
        self.dlg = QMessageBox()
        self.dlg.show()
        self.dlg.setIcon(QMessageBox.Information)
        self.dlg.setWindowTitle("Info")
        self.dlg.setText('Алле!')
        self.dlg.setInformativeText('Введите пару букв для поиска...')

    def select_comp(self):

        def new_thread(obj):
            comp = obj.tableWidget.currentIndex().data()
            command_session = str(f'quser /server:{comp}')
            proc = subprocess.run(command_session, stdout=subprocess.PIPE, encoding='cp866')
            id_session = proc.stdout
            id_session = re.findall(r' \d+', id_session)
            id_session = (str(id_session[0])).split(' '[0])
            id_session = id_session[1]
            print(id_session)
            command_rdp = f'mstsc /v {comp} /shadow:{id_session} /noConsentPrompt /control'
            # command = str('mstsc /v' + ' ' + comp + ' ' + '/shadow:1 /noConsentPrompt /control')
            subprocess.run(command_rdp)
        threading.Thread(target=new_thread, args=(self,)).start()

    def kill_excel(self):
        self.listWidget.clear()

        def excel(server):
            command_excel = str('taskkill /s' + ' ' + server + ' ' + '/IM excel.exe /f /t')
            output_excel = subprocess.Popen(command_excel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_excel, error_excel = output_excel.communicate()
            out_excel = out_excel.strip()
            error_excel = error_excel.strip()
            print(out_excel.decode('cp866'))
            print(error_excel.decode('cp866'))
            self.listWidget.addItem(str(out_excel.decode('cp866')))
            self.listWidget.addItem(str(error_excel.decode('cp866')))

        if self.checkBox.isChecked():
            excel(server='ia-sapp-fl01')
        if self.checkBox_1.isChecked():
            excel(server='ia-sapp-fl02')
        if self.checkBox_2.isChecked():
            excel(server='ia-sapp-fl03')
        if self.checkBox_3.isChecked():
            excel(server='ia-sapp-fl04')
        if self.checkBox_4.isChecked():
            excel(server='ia-sapp-fl05')
        if self.checkBox_5.isChecked():
            excel(server='ia-sapp-fl06')

        if self.checkBox_6.isChecked():
            excel(server='ia-sapp-ul01')
        if self.checkBox_7.isChecked():
            excel(server='ia-sapp-ul02')
        if self.checkBox_8.isChecked():
            excel(server='ia-sapp-ul03')

    def kill_word(self):
        self.listWidget.clear()

        def excel(server):
            command_word = str('taskkill /s' + ' ' + server + ' ' + '/IM winword.exe /f /t')
            output_word = subprocess.Popen(command_word, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_word, error_word = output_word.communicate()
            out_word = out_word.strip()
            error_word = error_word.strip()
            print(out_word.decode('cp866'))
            print(error_word.decode('cp866'))
            self.listWidget.addItem(str(out_word.decode('cp866')))
            self.listWidget.addItem(str(error_word.decode('cp866')))

        if self.checkBox.isChecked():
            excel(server='ia-sapp-fl01')
        if self.checkBox_1.isChecked():
            excel(server='ia-sapp-fl02')
        if self.checkBox_2.isChecked():
            excel(server='ia-sapp-fl03')
        if self.checkBox_3.isChecked():
            excel(server='ia-sapp-fl04')
        if self.checkBox_4.isChecked():
            excel(server='ia-sapp-fl05')
        if self.checkBox_5.isChecked():
            excel(server='ia-sapp-fl06')

        if self.checkBox_6.isChecked():
            excel(server='ia-sapp-ul01')
        if self.checkBox_7.isChecked():
            excel(server='ia-sapp-ul02')
        if self.checkBox_8.isChecked():
            excel(server='ia-sapp-ul03')

    def serv(self):

        def serv_start(server):
            command_excel = str('sc start' + ' ' + r'\\' + server + ' ' + '"DispatcherService"' + ' '
                                + 'obj= "' + server + r'\Администратор"' + ' ' + 'password= "!Eraser0" start= auto')
            # output_excel = subprocess.Popen(command_excel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out_excel, error_excel = output_excel.communicate()
            # out_excel = out_excel.strip()
            # error_excel = error_excel.strip()
            # print(out_excel.decode('cp866'))
            # print(error_excel.decode('cp866'))
            # self.listWidget.addItem(str(out_excel.decode('cp866')))
            # self.listWidget.addItem(str(error_excel.decode('cp866')))
            self.listWidget.addItem(str(command_excel))

        serv_start(server='ia-sapp-fl06')

    def on_start(self):
        threading.Thread(target=self.show_gif_start(), args=(self,)).start()

    def show_gif_start(self):
        self.dlg.show()
        self.label.setMovie(self.movie)
        self.movie.start()

    def show_gif_stop(self):
        self.movie.stop()
        self.dlg.close()

    def disc_c(self):

        def new_thread(obj):
            comp = obj.tableWidget.currentIndex().data()
            command_exp = str(fr'explorer \\{comp}\c$')
            proc = subprocess.run(command_exp, stdout=subprocess.PIPE, encoding='cp866')
        threading.Thread(target=new_thread, args=(self,)).start()

    def reboot(self):

        def new_thread(obj):
            comp = obj.tableWidget.currentIndex().data()
            command_exp = str(fr'shutdown /r /m \\{comp} /f')
            proc = subprocess.run(command_exp, stdout=subprocess.PIPE, encoding='cp866')
        threading.Thread(target=new_thread, args=(self,)).start()

    def edit_settings(self):
        self.child_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.child_window.show()
        config = self.load_settings()
        self.child_window.lineEdit.setText(config.get('username'))
        self.child_window.lineEdit_2.setText(config.get('password'))
        self.child_window.lineEdit_3.setText(config.get('ldap_url'))
        self.child_window.lineEdit_4.setText(config.get('search_base'))
        self.child_window.accepted.connect(self.accept_settings)

    def accept_settings(self):
        config = self.load_settings()
        config['username'] = self.child_window.lineEdit.text()
        config['password'] = self.child_window.lineEdit_2.text()
        config['ldap_url'] = self.child_window.lineEdit_3.text()
        config['search_base'] = self.child_window.lineEdit_4.text()
        with open('settings.yaml', 'w') as f:
            yaml.dump(config, f)
        self.load_settings()


class ChildWindow(QDialog, dlg.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParentWindow()
    window.show()
    app.exec()
