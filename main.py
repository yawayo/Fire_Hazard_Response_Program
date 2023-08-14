import sys
from PyQt5.QtWidgets    import *
from PyQt5.uic          import loadUi
from PyQt5.QtGui        import QIcon
from func_set           import func_set

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = loadUi("ui/system_ui.ui", self)
        self.setWindowIcon(QIcon("icon/hbrain.png"))
        self.fs = func_set(self.ui)
        #
        # sshFile = "ui/qdarkstyle/style.qss"
        # with open(sshFile, "r") as fh:
        #     self.setStyleSheet(fh.read())

    def resizeEvent(self, event):
        self.fs.resizeWidget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    #ex.showFullScreen()
    ex.show()
    ex.fs.resizeWidget()
    sys.exit(app.exec_())