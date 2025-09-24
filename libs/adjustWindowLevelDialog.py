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

        # Medical Presets section
        presets_group = QGroupBox("Medical Presets")
        presets_layout = QVBoxLayout()

        # Preset selection dropdown
        preset_selection_layout = QHBoxLayout()
        preset_selection_layout.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()

        # Define medical presets (width, level)
        self.medical_presets = {
            "Lung (肺がん)": (1500, -600),  # デフォルト: 肺がん用
            "Soft Tissue (軟組織)": (400, 40),
            "Bone (骨)": (1500, 400),
            "Abdomen (腹部)": (400, 50),
            "Brain (脳)": (100, 50),
            "Mediastinum (縦隔)": (500, 50),
            "Liver (肝臓)": (160, 60),
            "Custom (カスタム)": (1000, 200),
        }

        for preset_name in self.medical_presets.keys():
            self.preset_combo.addItem(preset_name)

        # Set default to lung cancer preset
        self.preset_combo.setCurrentText("Lung (肺がん)")
        self.preset_combo.currentTextChanged.connect(self.applyPreset)

        preset_selection_layout.addWidget(self.preset_combo)
        presets_layout.addLayout(preset_selection_layout)

        # Preset buttons for quick access
        preset_buttons_layout = QGridLayout()

        # Quick preset buttons
        self.lung_btn = QPushButton("肺がん")
        self.lung_btn.clicked.connect(lambda: self.applyNamedPreset("Lung (肺がん)"))
        self.lung_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.soft_tissue_btn = QPushButton("軟組織")
        self.soft_tissue_btn.clicked.connect(
            lambda: self.applyNamedPreset("Soft Tissue (軟組織)")
        )
        self.soft_tissue_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        self.bone_btn = QPushButton("骨")
        self.bone_btn.clicked.connect(lambda: self.applyNamedPreset("Bone (骨)"))
        self.bone_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: black;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)

        preset_buttons_layout.addWidget(self.lung_btn, 0, 0)
        preset_buttons_layout.addWidget(self.soft_tissue_btn, 0, 1)
        preset_buttons_layout.addWidget(self.bone_btn, 0, 2)
        presets_layout.addLayout(preset_buttons_layout)

        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)

        # Photometric Interpretation section
        photo_group = QGroupBox("Display Mode")
        photo_layout = QVBoxLayout()

        # Photometric interpretation info
        photo_info_layout = QHBoxLayout()
        photo_info_layout.addWidget(QLabel("Photometric:"))
        self.photo_info_label = QLabel("MONOCHROME2")
        self.photo_info_label.setStyleSheet("color: #666; font-weight: bold;")
        photo_info_layout.addWidget(self.photo_info_label)
        photo_info_layout.addStretch()
        photo_layout.addLayout(photo_info_layout)

        # Display mode controls
        display_mode_layout = QHBoxLayout()

        self.auto_invert_checkbox = QCheckBox("Auto (従来のPhotometric Interpretation)")
        self.auto_invert_checkbox.setChecked(
            True
        )  # デフォルトON: Photometric Interpretationを見るモード
        self.auto_invert_checkbox.stateChanged.connect(self.onDisplayModeChanged)

        self.force_invert_checkbox = QCheckBox("Force Invert (白黒反転)")
        self.force_invert_checkbox.stateChanged.connect(self.onDisplayModeChanged)

        display_mode_layout.addWidget(self.auto_invert_checkbox)
        display_mode_layout.addWidget(self.force_invert_checkbox)
        photo_layout.addLayout(display_mode_layout)

        # Explanation text
        explanation = QLabel("MONOCHROME1: 黒=高輝度, MONOCHROME2: 白=高輝度")
        explanation.setStyleSheet("font-size: 9pt; color: #888;")
        photo_layout.addWidget(explanation)

        photo_group.setLayout(photo_layout)
        layout.addWidget(photo_group)

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
        self.setFixedSize(
            450, 600
        )  # Increased size for medical presets and display mode

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

    def applyPreset(self, preset_name):
        """Apply selected medical preset"""
        if preset_name in self.medical_presets:
            width, level = self.medical_presets[preset_name]
            self.setValues(width, level)
            self.windowLevelChanged.emit(width, level)

    def applyNamedPreset(self, preset_name):
        """Apply preset by name and update combo box"""
        if preset_name in self.medical_presets:
            # Update combo box selection
            self.preset_combo.blockSignals(True)
            self.preset_combo.setCurrentText(preset_name)
            self.preset_combo.blockSignals(False)

            # Apply the preset
            self.applyPreset(preset_name)

    def popUp(self, w_width=None, w_level=None, move=True):
        # If no values provided, use lung cancer preset as default
        if w_width is None or w_level is None:
            w_width, w_level = self.medical_presets["Lung (肺がん)"]

        # Set initial values
        self.setValues(w_width, w_level)

        # Update combo box to reflect current preset
        for preset_name, (preset_width, preset_level) in self.medical_presets.items():
            if preset_width == w_width and preset_level == w_level:
                self.preset_combo.setCurrentText(preset_name)
                break
        else:
            self.preset_combo.setCurrentText("Custom (カスタム)")

        if move:
            self.move(QCursor.pos())

        # Show as non-modal dialog for real-time updates
        self.show()
        return None  # Non-modal, so no return value needed

    def resetValues(self):
        """Reset to lung cancer preset (default)"""
        lung_preset_values = self.medical_presets["Lung (肺がん)"]
        self.setValues(*lung_preset_values)
        self.preset_combo.setCurrentText("Lung (肺がん)")
        self.windowLevelChanged.emit(*lung_preset_values)

    def onDisplayModeChanged(self):
        """Handle display mode checkbox changes"""
        # Ensure only one checkbox is selected at a time
        sender = self.sender()

        if (
            sender == self.auto_invert_checkbox
            and self.auto_invert_checkbox.isChecked()
        ):
            self.force_invert_checkbox.blockSignals(True)
            self.force_invert_checkbox.setChecked(False)
            self.force_invert_checkbox.blockSignals(False)
        elif (
            sender == self.force_invert_checkbox
            and self.force_invert_checkbox.isChecked()
        ):
            self.auto_invert_checkbox.blockSignals(True)
            self.auto_invert_checkbox.setChecked(False)
            self.auto_invert_checkbox.blockSignals(False)
        elif (
            not self.auto_invert_checkbox.isChecked()
            and not self.force_invert_checkbox.isChecked()
        ):
            # At least one must be selected - default to auto
            self.auto_invert_checkbox.blockSignals(True)
            self.auto_invert_checkbox.setChecked(True)
            self.auto_invert_checkbox.blockSignals(False)

        # Emit signal to update image display
        width_value = self.window_slider.value()
        level_value = self.level_slider.value()
        self.windowLevelChanged.emit(width_value, level_value)

    def updatePhotometricInfo(self, dicom_path):
        """Update photometric interpretation info from DICOM file"""
        try:
            from libs.dicom_io import DICOMReader

            photometric = DICOMReader.getPhotometricInterpretation(dicom_path)
            self.photo_info_label.setText(photometric)
        except Exception:
            self.photo_info_label.setText("UNKNOWN")

    def getDisplayMode(self):
        """Get current display mode setting"""
        if self.force_invert_checkbox.isChecked():
            return True  # Force invert
        elif self.auto_invert_checkbox.isChecked():
            return None  # Auto (based on photometric interpretation)
        else:
            return False  # No invert

    def getCurrentValues(self):
        """Get current window/level values"""
        try:
            width = int(self.windowEdit.text())
            level = int(self.levelEdit.text())
            return width, level
        except ValueError:
            return self.window_slider.value(), self.level_slider.value()
