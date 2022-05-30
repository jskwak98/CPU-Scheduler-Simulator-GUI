import sys
from random import randint
from process import Process
from draw import ChartDrawer

from fcfs import FCFS
from sjf import SJF
from srtf import SRTF
from rr import RR
from priority import Priority
from priorityrr import PriorityRR
from preem_priority import PPriority

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtGui import QIntValidator

def scheduler_selector(selection):
    if selection == "FCFS":
        return FCFS
    elif selection == "SJF":
        return SJF
    elif selection == "SRTF":
        return SRTF
    elif selection == "RR":
        return RR
    elif selection == "NP-P":
        return Priority
    elif selection == "P-P":
        return PPriority
    elif selection == "NP-P-RR":
        return PriorityRR

def make_process_list(data):
    process_list = []
    for row in data:
        pid, a, s, p = row
        process_list.append(Process(pid, a, s, p))
    return process_list

class SimulatorGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        total_frame = QVBoxLayout()

        self.input_frame = InputPart()
        button_frame = self.createSimulateButtonGroup()
        self.result_frame = OutputPart()

        total_frame.addWidget(self.input_frame)
        total_frame.addWidget(button_frame)
        total_frame.addWidget(self.result_frame)

        self.setLayout(total_frame)

        self.setWindowTitle('CPU Scheduler Simulator')
        self.setGeometry(300, 300, 1250, 1100)
        self.center()
        self.show()

    def createSimulateButtonGroup(self):
        groupbox = QGroupBox()

        simulatebutton = QPushButton('Simulate')
        simulatebutton.clicked.connect(self.simulate)
        resetbutton = QPushButton('Reset')
        resetbutton.clicked.connect(self.reset)

        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(simulatebutton)
        hbox.addStretch(1)
        hbox.addWidget(resetbutton)
        hbox.addStretch(2)
        groupbox.setLayout(hbox)

        return groupbox

    def reset(self):
        self.input_frame.reset()
        if self.result_frame.to_erase:
            self.result_frame.reset()

    def simulate(self):
        if not self.input_frame.input_data:
            return

        # make process list based on the input data
        process_list = make_process_list(self.input_frame.input_data)

        # get an appropriate scheduler
        selection = self.input_frame.alg_selection.currentText()
        schedulerClass = scheduler_selector(selection)
        if selection in {"RR", "NP-P-RR"}:
            if not self.input_frame.time_quantum.text():
                QMessageBox.information(self, '시간할당량 미입력', '시간할당량을 필요로 하는 알고리즘입니다.')
                return
            scheduler = schedulerClass(process_list, int(self.input_frame.time_quantum.text()))
        else:
            scheduler = schedulerClass(process_list)

        # schedule
        schedule = scheduler.do_schedule()

        # draw gantt chart
        chart = self.result_frame.draw(schedule)
        self.result_frame.browser.setHtml(chart.to_html(include_plotlyjs='cdn'))

        # reflect result on board
        self.result_frame.reflect(process_list)



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class InputPart(QWidget):

    def __init__(self):
        super().__init__()
        self.input_data = []
        self.row_count = 0
        self.max_count = 10
        self.initUI()

    def initUI(self):
        input_frame = QHBoxLayout()
        groupbox = QGroupBox('Input 생성')

        # data manipulation
        manipulator_layout = QVBoxLayout()

        # selection 란
        alg_layout = QHBoxLayout()

        alg_label = QLabel("Algorithm")
        alg_label.setAlignment(Qt.AlignHCenter)
        alg_label.font().setBold(True)

        self.alg_selection = QComboBox()
        self.alg_selection.addItem('FCFS')
        self.alg_selection.addItem('SJF')
        self.alg_selection.addItem('SRTF')
        self.alg_selection.addItem('RR')
        self.alg_selection.addItem('NP-P')
        self.alg_selection.addItem('P-P')
        self.alg_selection.addItem('NP-P-RR')

        self.time_quantum = QLineEdit()
        self.time_quantum.setPlaceholderText('시간할당량')
        self.time_quantum.setValidator(QIntValidator(1, 20))

        alg_layout.addStretch(1)
        alg_layout.addWidget(alg_label)
        alg_layout.addStretch(1)
        alg_layout.addWidget(self.alg_selection)
        alg_layout.addStretch(1)
        alg_layout.addWidget(self.time_quantum)
        alg_layout.addStretch(1)

        # manual add 란
        proc_layout = QGridLayout()

        proc_layout.addWidget(QLabel('도착시간'), 0, 0)
        proc_layout.addWidget(QLabel('서비스시간'), 0, 1)
        proc_layout.addWidget(QLabel('우선순위'), 0, 2)

        self.arrival = QLineEdit()
        self.arrival.setValidator(QIntValidator(0, 50))
        self.arrival.setPlaceholderText('0 ~ 50')
        self.service = QLineEdit()
        self.service.setValidator(QIntValidator(1, 20))
        self.service.setPlaceholderText('1 ~ 20')
        self.priority = QLineEdit()
        self.priority.setValidator(QIntValidator(0, 9))
        self.priority.setPlaceholderText('0 ~ 9')

        proc_layout.addWidget(self.arrival, 1, 0)
        proc_layout.addWidget(self.service, 1, 1)
        proc_layout.addWidget(self.priority, 1, 2)

        # buttons
        manual_layout = QHBoxLayout()

        adder = QPushButton('추가')
        adder.clicked.connect(self.add_data)
        deleter = QPushButton('삭제')
        deleter.clicked.connect(self.delete_data)

        manual_layout.addStretch(2)
        manual_layout.addWidget(adder)
        manual_layout.addStretch(1)
        manual_layout.addWidget(deleter)
        manual_layout.addStretch(2)

        auto_layout = QHBoxLayout()

        random_adder = QPushButton('랜덤 입력')
        random_adder.clicked.connect(self.add_random_data)
        example_adder = QPushButton('예제 입력')
        example_adder.clicked.connect(self.add_example)

        auto_layout.addWidget(random_adder)
        auto_layout.addWidget(example_adder)

        # 합치기
        manipulator_layout.addStretch(3)
        manipulator_layout.addLayout(alg_layout)
        manipulator_layout.addStretch(3)
        manipulator_layout.addLayout(proc_layout)

        manipulator_layout.addLayout(manual_layout)
        manipulator_layout.addStretch(3)
        manipulator_layout.addLayout(auto_layout)
        manipulator_layout.addStretch(3)

        groupbox.setLayout(manipulator_layout)

        # input table
        table_groupbox = QGroupBox('프로세스 데이터')
        table_view = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        labels = ['PID', '도착시간', '서비스시간', '우선순위']
        self.table.setHorizontalHeaderLabels(labels)
        table_view.addWidget(self.table)
        table_groupbox.setLayout(table_view)

        # 최종 프레임
        input_frame.addWidget(groupbox)
        input_frame.addWidget(table_groupbox)

        self.setLayout(input_frame)

    def add_data(self):
        if self.arrival.text() and self.service.text() and self.priority.text():
            a = int(self.arrival.text())
            s = int(self.service.text())
            p = int(self.priority.text())

            self.add_with_val(a, s, p)
        else:
            return

    def delete_data(self):
        if self.row_count == 0:
            return
        self.row_count -= 1
        self.table.removeRow(self.row_count)
        self.table.setRowCount(self.max_count)
        self.input_data.pop()

    def add_random_data(self):
        a = randint(0, 50)
        s = randint(1, 20)
        p = randint(0, 4)
        self.add_with_val(a, s, p)

    def add_example(self):
        self.add_with_val(0, 10, 3)
        self.add_with_val(1, 28, 2)
        self.add_with_val(2, 6, 4)
        self.add_with_val(3, 4, 1)
        self.add_with_val(4, 14, 2)

    def add_with_val(self, a, s, p):
        # TODO input error handling, service는 burst보다 작거나 같다, 둘 모두 1 이상
        temp = []
        temp.append(f"P{self.row_count + 1}")
        temp.append(a)
        temp.append(s)
        temp.append(p)

        # increase max row
        if self.row_count + 1 == self.max_count:
            self.max_count += 1
            self.table.setRowCount(self.max_count)

        for col in range(4):
            self.table.setItem(self.row_count, col, QTableWidgetItem(str(temp[col])))

        self.input_data.append(temp)
        self.row_count += 1

    def reset(self):
        for _ in range(len(self.input_data)):
            self.delete_data()
        self.max_count = 10
        self.table.setRowCount(self.max_count)
        self.alg_selection.setCurrentIndex(0)
        self.time_quantum.setText("")
        self.arrival.setText("")
        self.service.setText("")
        self.priority.setText("")


class OutputPart(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.to_erase = False

    def initUI(self):
        # 전체 프레임 생성
        result_frame = QGridLayout()
        result_frame.setRowMinimumHeight(0, 320)
        result_frame.setRowMinimumHeight(1, 300)

        # 간트 차트
        chart_groupbox = QGroupBox("간트 차트")
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        broswer_view = QVBoxLayout()
        broswer_view.addWidget(self.browser)
        chart_groupbox.setLayout(broswer_view)

        # 평균 통계량
        avg_groupbox = QGroupBox('평균 통계량')

        avg_frame = QVBoxLayout()
        returns = QHBoxLayout()
        values = QHBoxLayout()

        # 평균 통계량 라벨
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

        # 평균 통계량 값
        self.avg_w = QLabel("0")
        self.avg_w.setAlignment(Qt.AlignHCenter)

        self.avg_t = QLabel("0")
        self.avg_t.setAlignment(Qt.AlignHCenter)

        self.avg_r = QLabel("0")
        self.avg_r.setAlignment(Qt.AlignHCenter)

        values.addStretch(3)
        values.addWidget(self.avg_w)
        values.addStretch(2)
        values.addWidget(self.avg_t)
        values.addStretch(2)
        values.addWidget(self.avg_r)
        values.addStretch(3)

        avg_frame.addStretch(1)
        avg_frame.addLayout(returns)
        avg_frame.addLayout(values)
        avg_frame.addStretch(1)

        avg_groupbox.setLayout(avg_frame)

        # 시뮬 결과 프로세스 별 반환값
        table_groupbox = QGroupBox('프로세스 별 통계')
        table_view = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        labels = ['PID', '대기시간', '반환시간', '응답시간']
        self.table.setHorizontalHeaderLabels(labels)
        table_view.addWidget(self.table)
        table_groupbox.setLayout(table_view)


        result_frame.addWidget(chart_groupbox, 0, 0, 1, 2)
        result_frame.addWidget(avg_groupbox, 1, 0)
        result_frame.addWidget(table_groupbox, 1, 1)

        self.setLayout(result_frame)

    def reflect(self, process_list):
        n = len(process_list)
        self.to_erase = True
        self.data_n = n
        rc = n if n >= 10 else 10
        self.table.setRowCount(rc)

        t_w, t_t, t_r = 0, 0, 0
        row = 0

        for p in process_list:
            pid, w, r, t = p.get_result().values()
            self.table.setItem(row, 0, QTableWidgetItem(pid))
            self.table.setItem(row, 1, QTableWidgetItem(str(w)))
            self.table.setItem(row, 2, QTableWidgetItem(str(t)))
            self.table.setItem(row, 3, QTableWidgetItem(str(r)))
            t_w += w
            t_t += t
            t_r += r
            row += 1

        self.avg_w.setText(str(t_w/n))
        self.avg_t.setText(str(t_t / n))
        self.avg_r.setText(str(t_r / n))

    def draw(self, schedule):
        cd = ChartDrawer(schedule)
        chart = cd.draw_gantt_chart()
        return chart

    def reset(self):
        self.avg_w.setText(str(0))
        self.avg_t.setText(str(0))
        self.avg_r.setText(str(0))

        for row in range(self.data_n-1, -1, -1):
            self.table.removeRow(row)
            self.table.setRowCount(10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimulatorGUI()
    sys.exit(app.exec_())