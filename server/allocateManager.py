# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5   |  2023/10/12   | Auto-generated (from ui/allocatorUI.ui)                         |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A  |  2023/10/12   | refactored, implemented basic features                          |
# +-------------+--------------+-----------------------------------------------------------------+

from bson.objectid import ObjectId
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import *
import configparser
import socket
import dbhandler
import json
import sys

cursor = dbhandler.DBHandler()
conf = configparser.ConfigParser()
conf.read("./allocatemgr.conf")


class IndividualSignal(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass


class SignalConnectionWorker(QThread):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((conf['DEFAULT']['SignalAddr'], int(conf['DEFAULT']['SignalPort'])))

    def run(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.combinator_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.combinator_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.establish_connection()
        self.setupUi()

    def establish_connection(self):
        self.combinator_1.connect((conf['DEFAULT']['ColorCombinator1Addr'],
                                   int(conf['DEFAULT']['ColorCombinator1Port'])))
        print(f"Connection established with 1: {conf['DEFAULT']['ColorCombinator1Addr']}, {int(conf['DEFAULT']['ColorCombinator1Port'])}")

        self.combinator_2.connect((conf['DEFAULT']['ColorCombinator2Addr'],
                                   int(conf['DEFAULT']['ColorCombinator2Port'])))
        print(f"Connection established with 2: {conf['DEFAULT']['ColorCombinator2Addr']}, {int(conf['DEFAULT']['ColorCombinator2Port'])}")

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(852, 490)
        self.centralwidget = QWidget(self)
        self.setWindowTitle("프론 - 서버 관리 도구")

        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.baseVertical = QVBoxLayout()
        self.topHorizontal = QHBoxLayout()
        self.buttomHorizontal = QHBoxLayout()

        self.filterLineEdit = QLineEdit(self.centralwidget)
        self.filterLineEdit.setToolTip("검색할 이름을 입력하세요 (비우면 모두 불러옴)")
        self.topHorizontal.addWidget(self.filterLineEdit)

        self.searchButton = QPushButton(self.centralwidget)
        self.searchButton.setText("검색")
        self.searchButton.clicked.connect(self.display_data)
        self.topHorizontal.addWidget(self.searchButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setText("삭제")
        self.topHorizontal.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(self.delete)

        # self.modifyButton = QPushButton(self.centralwidget)
        # self.modifyButton.setText("커밋")
        # self.topHorizontal.addWidget(self.modifyButton)

        self.baseVertical.addLayout(self.topHorizontal)
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.baseVertical.addWidget(self.tableWidget)

        self.alloc1Button = QPushButton(self.centralwidget)
        self.alloc1Button.setText("색조합기 1에 할당")
        self.alloc1Button.clicked.connect(lambda: self.allocate(1))
        self.buttomHorizontal.addWidget(self.alloc1Button)

        self.alloc2Button = QPushButton(self.centralwidget)
        self.alloc2Button.setText("색조합기 2에 할당")
        self.alloc2Button.clicked.connect(lambda: self.allocate(2))
        self.buttomHorizontal.addWidget(self.alloc2Button)

        self.tasklistButton = QPushButton(self.centralwidget)
        self.tasklistButton.setText("작업 목록 보기")
        self.buttomHorizontal.addWidget(self.tasklistButton)

        # self.status = QStatusBar(self.centralwidget)
        # self.setStatusBar(self.status)
        # self.status.showMessage("asdasf")

        self.baseVertical.addLayout(self.buttomHorizontal)
        self.verticalLayout_2.addLayout(self.baseVertical)
        self.setCentralWidget(self.centralwidget)

        self.display_data()

        self.show()

    def display_data(self):
        column_headers = ("데이터 ID", "크롬북 ID", "이름", "컬러코드", "상태")

        count, data = cursor.fetch_all()

        self.tableWidget.setRowCount(count)
        self.tableWidget.setColumnCount(len(column_headers))

        for index, datum in enumerate(data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(datum['_id'])))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(datum["ClientName"]))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(datum["data"]["CustomerName"]))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(str(datum["data"]["ColorCode"])))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(datum["status"]))

        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.resizeColumnsToContents()

    def allocate(self, to: int):
        if self.tableWidget.currentRow() == -1:
            return

        self.tableWidget.selectRow(self.tableWidget.currentRow())
        data = self.tableWidget.selectedItems()

        if to == 1:
            if data[4].text().startswith("inprogress"):
                QMessageBox.critical(self, "오류: 서버 관리 도구",
                                     f"작업 {data[0].text()}는 이미 색조합기 {data[4].text()[-1]}에 할당되었습니다.",
                                     QMessageBox.Yes, QMessageBox.Yes)
                return
            print("sending {} to 1".format(data[3].text()))
            cursor.update_status_by_id(ObjectId(data[0].text()), "inprogress1")
            # self.combinator_1.send(data[2].text().encode())

        elif to == 2:
            if data[4].text().startswith("inprogress"):
                QMessageBox.critical(self, "오류",
                                     f"작업 {data[0].text()}는 이미 색조합기 {data[4].text()[-1]}에 할당되었습니다.", QMessageBox.Yes,
                                     QMessageBox.Yes)
                return
            print("sending {} to 2".format(data[3].text()))
            cursor.update_status_by_id(ObjectId(data[0].text()), "inprogress2")
            # self.combinator_2.send(data[2].text().encode())

        QMessageBox.information(self, "성공",
                    f"작업 {data[0].text()}가 색조합기 {to}에 잘 할당되었습니다.\n색조합이 곧 시작됩니다.",
                    QMessageBox.Yes, QMessageBox.Yes)

        self.display_data()
        self.tableWidget.clearSelection()

    def delete(self):
        if self.tableWidget.currentRow() == -1:
            return

        self.tableWidget.selectRow(self.tableWidget.currentRow())
        data = self.tableWidget.selectedItems()

        if data[4].text().startswith("inprogress"):
            QMessageBox.critical(self, "오류",
                                 f"작업 {data[0].text()}는 현재 조합중인 작업입니다.\n삭제할 수 없습니다.",
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        cursor.delete_data_by_id(ObjectId(data[0].text()))
        QMessageBox.information(self, "성공",
                                f"작업 {data[0].text()}가 잘 지워졌습니다.",
                                QMessageBox.Ok, QMessageBox.Ok)

        self.display_data()


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
