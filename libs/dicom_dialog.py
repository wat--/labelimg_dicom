try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import newIcon, labelValidator

BB = QDialogButtonBox


class DICOMDialog(QDialog):

    def __init__(self, parent=None, listItem=None):
        super(DICOMDialog, self).__init__(parent)

        self.selected_idx = 0

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)

        layout = QVBoxLayout()
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def popUp(self, text='', move=True):
        if move:
            self.move(QCursor.pos())
        return self.selected_idx if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        self.selected_idx = self.listWidget.selectedIndexes()[0].row()

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.accept()
