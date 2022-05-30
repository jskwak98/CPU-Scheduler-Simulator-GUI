import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWebEngineWidgets

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
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        result_frame = QHBoxLayout()
        result_frame.addLayout(self.createAverage())
        result_frame.addWidget(self.createOutputProcessTable())

        total_frame.addLayout(input_frame)
        total_frame.addWidget(button_frame)
        total_frame.addWidget(self.browser)
        total_frame.addLayout(result_frame)


        self.setLayout(total_frame)

        self.setWindowTitle('CPU Scheduler Simulator')
        self.setGeometry(300, 300, 1200, 900)
        self.center()
        self.show()

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
        labels = ['PID', '도착시간', '서비스시간', '우선순위', '시간할당량']
        table.setHorizontalHeaderLabels(labels)

        return table

    def createAverage(self):
        total_frame = QVBoxLayout()
        returns = QHBoxLayout()
        values = QHBoxLayout()

        avg_w_label = QLabel("평균대기시간")
        avg_w_label.setAlignment(Qt.AlignHCenter)

        avg_t_labels = QLabel("평균반환시간")
        avg_t_labels.setAlignment(Qt.AlignHCenter)

        avg_r_labels = QLabel("평균응답시간")
        avg_r_labels.setAlignment(Qt.AlignHCenter)

        returns.addStretch(3)
        returns.addWidget(avg_w_label)
        returns.addStretch(2)
        returns.addWidget(avg_t_labels)
        returns.addStretch(2)
        returns.addWidget(avg_r_labels)
        returns.addStretch(3)

        avg_w = QLabel("0")
        avg_w.setAlignment(Qt.AlignHCenter)

        avg_t = QLabel("0")
        avg_t.setAlignment(Qt.AlignHCenter)

        avg_r = QLabel("0")
        avg_r.setAlignment(Qt.AlignHCenter)

        values.addStretch(3)
        values.addWidget(avg_w)
        values.addStretch(2)
        values.addWidget(avg_t)
        values.addStretch(2)
        values.addWidget(avg_r)
        values.addStretch(3)

        total_frame.addStretch(1)
        total_frame.addLayout(returns)
        total_frame.addLayout(values)
        total_frame.addStretch(1)

        return total_frame

    def createOutputProcessTable(self):
        table = QTableWidget()
        table.setRowCount(10)
        table.setColumnCount(4)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        labels = ['PID', '대기시간', '반환시간', '응답시간']
        table.setHorizontalHeaderLabels(labels)

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
