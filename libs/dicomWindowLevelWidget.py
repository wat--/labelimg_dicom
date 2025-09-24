#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


class DicomWindowLevelWidget(QWidget):
    """Widget for DICOM Window/Level adjustment with sliders"""

    windowLevelChanged = pyqtSignal(int, int)  # width, level

    def __init__(self, parent=None):
        super(DicomWindowLevelWidget, self).__init__(parent)
        self.setWindowTitle("DICOM Window/Level")
        self.setupUI()
        self.setVisible(False)  # Hidden by default

    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # Title
        title = QLabel("DICOM Window/Level")
        title.setStyleSheet("font-weight: bold; color: #2E86AB;")
        layout.addWidget(title)

        # Window Width controls
        width_layout = QHBoxLayout()
        width_label = QLabel("Width:")
        width_label.setMinimumWidth(50)
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(1, 4000)
        self.width_slider.setValue(1000)
        self.width_value_label = QLabel("1000")
        self.width_value_label.setMinimumWidth(50)
        self.width_value_label.setAlignment(Qt.AlignCenter)
        self.width_value_label.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #ccc; padding: 2px;"
        )

        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_slider)
        width_layout.addWidget(self.width_value_label)
        layout.addLayout(width_layout)

        # Window Level controls
        level_layout = QHBoxLayout()
        level_label = QLabel("Level:")
        level_label.setMinimumWidth(50)
        self.level_slider = QSlider(Qt.Horizontal)
        self.level_slider.setRange(-1000, 3000)
        self.level_slider.setValue(200)
        self.level_value_label = QLabel("200")
        self.level_value_label.setMinimumWidth(50)
        self.level_value_label.setAlignment(Qt.AlignCenter)
        self.level_value_label.setStyleSheet(
            "background-color: #f0f0f0; border: 1px solid #ccc; padding: 2px;"
        )

        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_slider)
        level_layout.addWidget(self.level_value_label)
        layout.addLayout(level_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.auto_adjust_btn = QPushButton("Auto")
        self.auto_adjust_btn.setMaximumWidth(50)
        self.auto_adjust_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setMaximumWidth(50)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        button_layout.addWidget(self.auto_adjust_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect signals
        self.width_slider.valueChanged.connect(self.on_width_changed)
        self.level_slider.valueChanged.connect(self.on_level_changed)
        self.auto_adjust_btn.clicked.connect(self.auto_adjust_requested)
        self.reset_btn.clicked.connect(self.reset_values)

        # Set fixed size
        self.setFixedSize(250, 120)

        # Style the widget
        self.setStyleSheet("""
            DicomWindowLevelWidget {
                background-color: rgba(240, 240, 240, 220);
                border: 2px solid #2E86AB;
                border-radius: 8px;
            }
        """)

    def on_width_changed(self, value):
        self.width_value_label.setText(str(value))
        self.windowLevelChanged.emit(value, self.level_slider.value())

    def on_level_changed(self, value):
        self.level_value_label.setText(str(value))
        self.windowLevelChanged.emit(self.width_slider.value(), value)

    def set_values(self, width, level):
        """Set slider values without triggering signals"""
        self.width_slider.blockSignals(True)
        self.level_slider.blockSignals(True)

        self.width_slider.setValue(width)
        self.level_slider.setValue(level)
        self.width_value_label.setText(str(width))
        self.level_value_label.setText(str(level))

        self.width_slider.blockSignals(False)
        self.level_slider.blockSignals(False)

    def get_values(self):
        """Get current slider values"""
        return self.width_slider.value(), self.level_slider.value()

    def reset_values(self):
        """Reset to default values"""
        self.set_values(1000, 200)
        self.windowLevelChanged.emit(1000, 200)

    def auto_adjust_requested(self):
        """Signal that auto-adjust is requested"""
        # This will be connected to the main window's auto-adjust method
        pass
