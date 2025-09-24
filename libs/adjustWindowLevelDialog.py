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
    # Signal for real-time updates
    windowLevelChanged = pyqtSignal(int, int)  # width, level

    def __init__(self, text="Adjust window/level", parent=None):
        super(AdjustWindowLevelDialog, self).__init__(parent)

        self.parent_window = parent
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("DICOM Window/Level Adjustment")
        self.setModal(False)  # Non-modal dialog for real-time updates

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Window Width section
        window_group = QGroupBox("Window Width")
        window_layout = QVBoxLayout()

        # Window slider
        self.window_slider = QSlider(Qt.Horizontal)
        self.window_slider.setRange(1, 20000)
        self.window_slider.setValue(1000)
        self.window_slider.valueChanged.connect(self.onWindowChanged)

        # Window value display
        window_value_layout = QHBoxLayout()
        window_value_layout.addWidget(QLabel("Value:"))
        self.windowEdit = QLineEdit()
        self.windowEdit.setText("1000")
        self.windowEdit.setValidator(labelValidator())
        self.windowEdit.editingFinished.connect(self.onWindowEditFinished)
        window_value_layout.addWidget(self.windowEdit)

        window_layout.addWidget(self.window_slider)
        window_layout.addLayout(window_value_layout)
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)

        # Level section
        level_group = QGroupBox("Window Level")
        level_layout = QVBoxLayout()

        # Level slider
        self.level_slider = QSlider(Qt.Horizontal)
        self.level_slider.setRange(-10000, 10000)
        self.level_slider.setValue(200)
        self.level_slider.valueChanged.connect(self.onLevelChanged)

        # Level value display
        level_value_layout = QHBoxLayout()
        level_value_layout.addWidget(QLabel("Value:"))
        self.levelEdit = QLineEdit()
        self.levelEdit.setText("200")
        self.levelEdit.setValidator(labelValidator())
        self.levelEdit.editingFinished.connect(self.onLevelEditFinished)
        level_value_layout.addWidget(self.levelEdit)

        level_layout.addWidget(self.level_slider)
        level_layout.addLayout(level_value_layout)
        level_group.setLayout(level_layout)
        layout.addWidget(level_group)

        # Buttons section
        button_layout = QHBoxLayout()

        # Auto adjust button
        self.auto_btn = QPushButton("Auto Adjust")
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.auto_btn.clicked.connect(self.autoAdjust)

        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.reset_btn.clicked.connect(self.resetValues)

        button_layout.addWidget(self.auto_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # OK/Cancel buttons
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon("done"))
        bb.button(BB.Cancel).setIcon(newIcon("undo"))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        self.setLayout(layout)
        self.setFixedSize(350, 300)

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

    def onWindowChanged(self, value):
        """Handle window width slider changes"""
        self.windowEdit.blockSignals(True)
        self.windowEdit.setText(str(value))
        self.windowEdit.blockSignals(False)

        # Emit signal for real-time update
        level_value = self.level_slider.value()
        self.windowLevelChanged.emit(value, level_value)

    def onLevelChanged(self, value):
        """Handle window level slider changes"""
        self.levelEdit.blockSignals(True)
        self.levelEdit.setText(str(value))
        self.levelEdit.blockSignals(False)

        # Emit signal for real-time update
        width_value = self.window_slider.value()
        self.windowLevelChanged.emit(width_value, value)

    def onWindowEditFinished(self):
        """Handle window width text edit changes"""
        try:
            value = int(self.windowEdit.text())
            value = max(1, min(value, 20000))  # Clamp to valid range

            self.window_slider.blockSignals(True)
            self.window_slider.setValue(value)
            self.window_slider.blockSignals(False)

            self.windowEdit.setText(str(value))

            # Emit signal for real-time update
            level_value = self.level_slider.value()
            self.windowLevelChanged.emit(value, level_value)
        except ValueError:
            # Reset to slider value if invalid input
            self.windowEdit.setText(str(self.window_slider.value()))

    def onLevelEditFinished(self):
        """Handle window level text edit changes"""
        try:
            value = int(self.levelEdit.text())
            value = max(-10000, min(value, 10000))  # Clamp to valid range

            self.level_slider.blockSignals(True)
            self.level_slider.setValue(value)
            self.level_slider.blockSignals(False)

            self.levelEdit.setText(str(value))

            # Emit signal for real-time update
            width_value = self.window_slider.value()
            self.windowLevelChanged.emit(width_value, value)
        except ValueError:
            # Reset to slider value if invalid input
            self.levelEdit.setText(str(self.level_slider.value()))

    def autoAdjust(self):
        """Request auto adjustment from parent window"""
        if hasattr(self.parent_window, "autoAdjustDicomWindow"):
            self.parent_window.autoAdjustDicomWindow()
            # Update sliders with new values
            self.setValues(
                self.parent_window.dicomWindowWidth, self.parent_window.dicomWindowLevel
            )

    def resetValues(self):
        """Reset to default values"""
        self.setValues(1000, 200)
        self.windowLevelChanged.emit(1000, 200)

    def setValues(self, width, level):
        """Set slider and text values without triggering signals"""
        # Block all signals temporarily
        self.window_slider.blockSignals(True)
        self.level_slider.blockSignals(True)
        self.windowEdit.blockSignals(True)
        self.levelEdit.blockSignals(True)

        # Update values
        self.window_slider.setValue(width)
        self.level_slider.setValue(level)
        self.windowEdit.setText(str(width))
        self.levelEdit.setText(str(level))

        # Re-enable signals
        self.window_slider.blockSignals(False)
        self.level_slider.blockSignals(False)
        self.windowEdit.blockSignals(False)
        self.levelEdit.blockSignals(False)

    def popUp(self, w_width=1000, w_level=200, move=True):
        # Set initial values
        self.setValues(w_width, w_level)

        if move:
            self.move(QCursor.pos())

        # Show as non-modal dialog for real-time updates
        self.show()
        return None  # Non-modal, so no return value needed

    def getCurrentValues(self):
        """Get current window/level values"""
        try:
            width = int(self.windowEdit.text())
            level = int(self.levelEdit.text())
            return width, level
        except ValueError:
            return self.window_slider.value(), self.level_slider.value()
