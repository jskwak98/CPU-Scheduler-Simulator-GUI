import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class SimulatorGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        total_frame = QVBoxLayout()
        input_frame = QHBoxLayout()

        input_frame.addWidget(self.createInputGroup())
        input_frame.addWidget(self.createInputProcessTable())

        button_frame = self.createSimulateButtonGroup()

        total_frame.addLayout(input_frame)
        total_frame.addWidget(button_frame)
        #total_frame.addWidget(self.createChart()) # QTableWidget
        #total_frame.addWidget(self.createAverage())
        #total_frame.addWidget(self.createOutputProcessTable())

        self.setLayout(total_frame)

        self.setWindowTitle('CPU Scheduler Simulator')
        self.setGeometry(300, 300, 1200, 400)
        self.center()
        self.show()

        # grid = QGridLayout()
        # grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        # grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        # grid.addWidget(self.createSimulateButtonGroup(), 1, 0)
        # grid.addWidget(self.createSecondExclusiveGroup(), 2, 0)
        # grid.addWidget(self.createPushButtonGroup(), 2, 1)
        #
        # self.setLayout(grid)
        #
        # self.setWindowTitle('Box Layout')
        # self.setGeometry(300, 300, 480, 320)
        # self.show()

    def createSimulateButtonGroup(self):
        groupbox = QGroupBox()

        simulatebutton = QPushButton('Simulate')
        resetbutton = QPushButton('Reset')

        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(simulatebutton)
        hbox.addStretch(1)
        hbox.addWidget(resetbutton)
        hbox.addStretch(2)
        groupbox.setLayout(hbox)

        return groupbox

    def createInputGroup(self):
        groupbox = QGroupBox('Input 생성')

        # total frame
        total_layout = QVBoxLayout()

        # selection 란
        alg_layout = QHBoxLayout()

        alg_label = QLabel("Algorithm")
        alg_label.setAlignment(Qt.AlignHCenter)
        alg_label.font().setBold(True)

        alg_selection = QComboBox()
        alg_selection.addItem('FCFS')
        alg_selection.addItem('SJF')
        alg_selection.addItem('SRTF')
        alg_selection.addItem('RR')
        alg_selection.addItem('NP-P')
        alg_selection.addItem('P-P')
        alg_selection.addItem('NP-P-RR')

        alg_layout.addWidget(alg_label)
        alg_layout.addWidget(alg_selection)

        # manual add 란
        proc_layout = QGridLayout()

        proc_layout.addWidget(QLabel('도착시간'), 0, 0)
        proc_layout.addWidget(QLabel('서비스시간'), 0, 1)
        proc_layout.addWidget(QLabel('우선순위'), 0, 2)
        proc_layout.addWidget(QLabel('시간할당량'), 0, 3)

        proc_layout.addWidget(QLineEdit(), 1, 0)
        proc_layout.addWidget(QLineEdit(), 1, 1)
        proc_layout.addWidget(QLineEdit(), 1, 2)
        proc_layout.addWidget(QLineEdit(), 1, 3)

        # buttons
        manual_layout = QHBoxLayout()

        manual_layout.addStretch(2)
        manual_layout.addWidget(QPushButton('추가'))
        manual_layout.addStretch(1)
        manual_layout.addWidget(QPushButton('삭제'))
        manual_layout.addStretch(2)

        auto_layout = QHBoxLayout()

        auto_layout.addWidget(QPushButton('랜덤 입력'))
        auto_layout.addWidget(QPushButton('예제 입력'))

        # 합치기
        total_layout.addStretch(3)
        total_layout.addLayout(alg_layout)
        total_layout.addStretch(3)
        total_layout.addLayout(proc_layout)

        total_layout.addLayout(manual_layout)
        total_layout.addStretch(3)
        total_layout.addLayout(auto_layout)
        total_layout.addStretch(3)

        groupbox.setLayout(total_layout)

        return groupbox

    def createInputProcessTable(self):
        table = QTableWidget()
        table.setRowCount(10)
        table.setColumnCount(5)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        return table

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimulatorGUI()
    sys.exit(app.exec_())
