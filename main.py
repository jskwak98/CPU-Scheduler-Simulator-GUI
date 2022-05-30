from GUI import SimulatorGUI
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
ex = SimulatorGUI()
sys.exit(app.exec_())
