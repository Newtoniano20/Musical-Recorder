from src import *
import sys
import logging


def main():
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')
    _win = MainWindow()
    _win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting App"
                 "")
    main()
