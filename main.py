import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from game import UltimateTicTacToe
def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Ultimate Tic-Tac-Toe")
    QApplication.setWindowIcon(QIcon("icon.jpg"))
    ex = UltimateTicTacToe()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
