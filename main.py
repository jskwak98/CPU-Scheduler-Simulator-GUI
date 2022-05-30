from GUI import SimulatorGUI
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimulatorGUI()
    sys.exit(app.exec_())