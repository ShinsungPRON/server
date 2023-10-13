# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5   |  2023/10/12   | Auto-generated (from ui/allocatorUI.ui)                         |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A  |  2023/10/12   | refactored, implemented basic features                          |
# +-------------+--------------+-----------------------------------------------------------------+

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
import configparser
import socket
import dbhandler
import json
import sys

# testdata = [
#     {
#         "ID": 0,
#         "ClientName": "CHROMEBOOK_01",
#         "data": {
#             "CustomerName": "안동기",
#             "ColorCode": "FFFFFF"
#         },
#         "status": "waiting"
#     },
#     {
#         "ID": 1,
#         "ClientName": "CHROMEBOOK_03",
#         "data": {
#             "CustomerName": "박성현",
#             "ColorCode": "EDEDED"
#         },
#         "status": "inprogress"
#     },
#     {
#         "ID": 3,
#         "ClientName": "CHROMEBOOK_02",
#         "data": {
#             "CustomerName": "윤지운",
#             "ColorCode": "888888"
#         },
#         "status": "waiting"
#     }
# ]

cursor = dbhandler.DBHandler()


class IndividualSignal(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass


class SignalConnectionWorker(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conf = configparser.ConfigParser()
        self.conf.read("./allocatemgr.conf")

        self.combinator_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.combinator_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.establish_connection()
        self.setupUi()

    def establish_connection(self):
        self.combinator_1.connect((self.conf['DEFAULT']['ColorCombinator1Addr'],
                                   int(self.conf['DEFAULT']['ColorCombinator1Port'])))
        print(f"Connection established with 1: {self.conf['DEFAULT']['ColorCombinator1Addr']}, {int(self.conf['DEFAULT']['ColorCombinator1Port'])}")

        self.combinator_2.connect((self.conf['DEFAULT']['ColorCombinator2Addr'],
                                   int(self.conf['DEFAULT']['ColorCombinator2Port'])))
        print(f"Connection established with 2: {self.conf['DEFAULT']['ColorCombinator2Addr']}, {int(self.conf['DEFAULT']['ColorCombinator2Port'])}")

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

        self.modifyButton = QPushButton(self.centralwidget)
        self.modifyButton.setText("커밋")
        self.topHorizontal.addWidget(self.modifyButton)

        self.baseVertical.addLayout(self.topHorizontal)
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.baseVertical.addWidget(self.tableWidget)

        self.alloc1Button = QPushButton(self.centralwidget)
        self.alloc1Button.setText("1에 할당")
        self.alloc1Button.clicked.connect(lambda: self.allocate(1))
        self.buttomHorizontal.addWidget(self.alloc1Button)

        self.alloc2Button = QPushButton(self.centralwidget)
        self.alloc2Button.setText("2에 할당")
        self.alloc2Button.clicked.connect(lambda: self.allocate(2))
        self.buttomHorizontal.addWidget(self.alloc2Button)

        self.tasklistButton = QPushButton(self.centralwidget)
        self.tasklistButton.setText("작업 목록 보기")
        self.buttomHorizontal.addWidget(self.tasklistButton)

        self.baseVertical.addLayout(self.buttomHorizontal)
        self.verticalLayout_2.addLayout(self.baseVertical)
        self.setCentralWidget(self.centralwidget)

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
            print("sending {} to 1".format(data[2]))
            # self.combinator_1.send(data[2].text().encode())
        elif to == 2:
            print("sending {} to 2".format(data[2]))
            # self.combinator_2.send(data[2].text().encode())

    def delete(self):
        if self.tableWidget.currentRow() == -1:
            return

        self.tableWidget.selectRow(self.tableWidget.currentRow())
        data = self.tableWidget.selectedItems()

        # TODO: DB에서 지우기 기능 구현


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())