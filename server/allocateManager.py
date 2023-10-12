# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5   |  2023/10/12   | Auto-generated (from ui/allocatorUI.ui)                         |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A  |  2023/10/12   | refactored, implemented basic features                          |
# +-------------+--------------+-----------------------------------------------------------------+

from PyQt5.QtWidgets import *
import sys

testdata = [
    {
        "ID": 0,
        "ClientName": "CHROMEBOOK_01",
        "data": {
            "CustomerName": "안동기",
            "ColorCode": "FFFFFF"
        },
        "status": "waiting"
    },
    {
        "ID": 1,
        "ClientName": "CHROMEBOOK_03",
        "data": {
            "CustomerName": "박성현",
            "ColorCode": "EDEDED"
        },
        "status": "inprogress"
    },
    {
        "ID": 3,
        "ClientName": "CHROMEBOOK_02",
        "data": {
            "CustomerName": "윤지운",
            "ColorCode": "888888"
        },
        "status": "waiting"
    }
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

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
        self.searchButton.clicked.connect(lambda: self.display_data(testdata))
        self.topHorizontal.addWidget(self.searchButton)

        self.modifyButton = QPushButton(self.centralwidget)
        self.modifyButton.setText("수정")
        self.topHorizontal.addWidget(self.modifyButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setText("삭제")
        self.topHorizontal.addWidget(self.deleteButton)

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

    def display_data(self, data: list):
        column_headers = ("크롬북 ID", "이름", "컬러코드", "상태")
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(column_headers))

        for index, datum in enumerate(data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(datum["ClientName"]))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(datum["data"]["CustomerName"]))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(datum["data"]["ColorCode"])))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(datum["status"]))

        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.resizeColumnsToContents()

    def allocate(self, to: int):
        if self.tableWidget.currentRow() == -1:
            return

        self.tableWidget.selectRow(self.tableWidget.currentRow())
        data = self.tableWidget.selectedItems()

        # TODO: 할당 구현

    def delete(self):
        if self.tableWidget.currentRow() == -1:
            return

        self.tableWidget.selectRow(self.tableWidget.currentRow())
        data = self.tableWidget.selectedItems()

        # TODO: DB에서 지우기 기능 구현


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())