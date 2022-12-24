from src import *
import sys


def main():
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')
    _win = MainWindow()
    _win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logger.info("Starting App")
    main()
