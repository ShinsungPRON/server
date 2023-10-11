# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5   |  2023/10/12   | Auto-generated (from ui/allocatorUI.ui)                         |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A  |  2023/10/12   | refactored                                                      |
# +-------------+--------------+-----------------------------------------------------------------+

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys


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
        self.topHorizontal.addWidget(self.searchButton)

        self.modifyButton = QPushButton(self.centralwidget)
        self.modifyButton.setText("수정")
        self.topHorizontal.addWidget(self.modifyButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setText("삭제")
        self.topHorizontal.addWidget(self.deleteButton)

        self.baseVertical.addLayout(self.topHorizontal)
        self.tableView = QTableView(self.centralwidget)
        self.baseVertical.addWidget(self.tableView)


        self.alloc1Button = QPushButton(self.centralwidget)
        self.alloc1Button.setText("1에 할당")
        self.buttomHorizontal.addWidget(self.alloc1Button)

        self.alloc2Button = QPushButton(self.centralwidget)
        self.alloc2Button.setText("2에 할당")
        self.buttomHorizontal.addWidget(self.alloc2Button)

        self.tasklistButton = QPushButton(self.centralwidget)
        self.tasklistButton.setText("작업 목록 보기")
        self.buttomHorizontal.addWidget(self.tasklistButton)

        self.baseVertical.addLayout(self.buttomHorizontal)
        self.verticalLayout_2.addLayout(self.baseVertical)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())