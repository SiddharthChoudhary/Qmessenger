from PyQt5 import QtCore
class updateGuiThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(updateGuiThread, self).__init__(parent)
        self.start()
    def run(self):
        self.emit(QtCore.SIGNAL("progress(int, int)"), i + 1, len(something_iterable))
    def __del__(self):
        self.exiting = True
        self.wait()