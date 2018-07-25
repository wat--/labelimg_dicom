try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import newIcon, labelValidator

BB = QDialogButtonBox


class AdjustWindowLevelDialog(QDialog):

    def __init__(self, text="Adjust window/level", parent=None):
        super(AdjustWindowLevelDialog, self).__init__(parent)

        self.windowEdit = QLineEdit()
        self.windowEdit.setText(text)
        self.windowEdit.setValidator(labelValidator())
        self.windowEdit.editingFinished.connect(self.postProcess)

        self.levelEdit = QLineEdit()
        self.levelEdit.setText(text)
        self.levelEdit.setValidator(labelValidator())
        self.levelEdit.editingFinished.connect(self.postProcess)

        layout = QVBoxLayout()
        layout.addWidget(self.windowEdit)
        layout.addWidget(self.levelEdit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        self.setLayout(layout)

    def validate(self):
        try:
            if self.windowEdit.text().trimmed() and self.levelEdit.text().trimmed():
                try:
                    _ = int(self.windowEdit.text())
                    _ = int(self.levelEdit.text())
                    self.accept()
                except ValueError:
                    self.reject()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.windowEdit.text().strip() and self.levelEdit.text().strip():
                try:
                    _ = int(self.windowEdit.text())
                    _ = int(self.levelEdit.text())
                    self.accept()
                except ValueError:
                    self.reject()

    def postProcess(self):
        try:
            self.windowEdit.setText(self.windowEdit.text().trimmed())
            self.levelEdit.setText(self.levelEdit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.windowEdit.setText(self.windowEdit.text().strip())
            self.levelEdit.setText(self.levelEdit.text().strip())

    def popUp(self, w_width=1000, w_level=200, move=True):
        self.windowEdit.setText(str(w_width))
        self.windowEdit.setSelection(0, len(str(w_width)))
        self.windowEdit.setFocus(Qt.PopupFocusReason)

        self.levelEdit.setText(str(w_level))

        if move:
            self.move(QCursor.pos())

        if self.exec_():
            return int(self.windowEdit.text()), int(self.levelEdit.text())
        else:
            return None
