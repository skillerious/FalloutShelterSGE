import os
import json
from PyQt5 import QtWidgets, QtCore

def get_settings_path():
    """
    Returns the full path to the settings JSON file.
    On Windows, the file is stored in %APPDATA%/FalloutShelterSaveEditor/settings.json.
    On other systems, it is stored in ~/FalloutShelterSaveEditor/settings.json.
    """
    if os.name == 'nt':
        appdata_dir = os.getenv("APPDATA")
    else:
        appdata_dir = os.path.expanduser("~")
    settings_dir = os.path.join(appdata_dir, "FalloutShelterSaveEditor")
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    return os.path.join(settings_dir, "settings.json")

class Settings:
    def __init__(self):
        self.settings_file = get_settings_path()
        self.default_options = {
            "theme": "dark_teal",
            "auto_save": True,
            "show_notifications": True,
            "log_level": "Info",
            "last_opened_file": "",
            "recent_files": [],
            "debug_mode": False
        }
        # Start with defaults then load (if available) to override.
        self.options = self.default_options.copy()
        self.load()

    def load(self):
        """Load settings from the JSON file, if it exists."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    data = json.load(f)
                    self.options.update(data)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save(self):
        """Save the current settings to the JSON file."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.options, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def set_option(self, key, value):
        """Set a setting option and immediately save it."""
        self.options[key] = value
        self.save()

    def get_option(self, key, default=None):
        """Retrieve a setting option."""
        return self.options.get(key, default)

    def reset_to_defaults(self):
        """Reset all settings to their default values."""
        self.options = self.default_options.copy()
        self.save()

class SettingsDialog(QtWidgets.QDialog):
    """
    A settings dialog using a multi-tabbed layout.
    Uses qt-material styling if applied to the QApplication.
    """
    def __init__(self, settings, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.resize(600, 400)
        self.initUI()

    def initUI(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Create a QTabWidget to hold different settings categories
        self.tabWidget = QtWidgets.QTabWidget()
        mainLayout.addWidget(self.tabWidget)

        # Create individual tabs
        self.generalTab = self.createGeneralTab()
        self.appearanceTab = self.createAppearanceTab()
        self.advancedTab = self.createAdvancedTab()

        self.tabWidget.addTab(self.generalTab, "General")
        self.tabWidget.addTab(self.appearanceTab, "Appearance")
        self.tabWidget.addTab(self.advancedTab, "Advanced")

        # Bottom button row
        buttonLayout = QtWidgets.QHBoxLayout()
        self.resetBtn = QtWidgets.QPushButton("Reset to Defaults")
        self.resetBtn.clicked.connect(self.resetDefaults)
        buttonLayout.addWidget(self.resetBtn)
        buttonLayout.addStretch(1)
        self.cancelBtn = QtWidgets.QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.reject)
        buttonLayout.addWidget(self.cancelBtn)
        self.applyBtn = QtWidgets.QPushButton("Apply")
        self.applyBtn.clicked.connect(self.applySettings)
        buttonLayout.addWidget(self.applyBtn)
        mainLayout.addLayout(buttonLayout)

        self.loadSettingsIntoUI()

    def createGeneralTab(self):
        """Creates the 'General' settings tab."""
        tab = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout(tab)
        
        self.autoSaveCheckbox = QtWidgets.QCheckBox("Enable Auto Save")
        formLayout.addRow("Auto Save:", self.autoSaveCheckbox)
        
        self.showNotificationsCheckbox = QtWidgets.QCheckBox("Show Notifications")
        formLayout.addRow("Notifications:", self.showNotificationsCheckbox)
        
        # Display-only fields for file information
        self.lastOpenedFileEdit = QtWidgets.QLineEdit()
        self.lastOpenedFileEdit.setReadOnly(True)
        formLayout.addRow("Last Opened File:", self.lastOpenedFileEdit)
        
        self.recentFilesList = QtWidgets.QListWidget()
        self.recentFilesList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        formLayout.addRow("Recent Files:", self.recentFilesList)
        
        return tab

    def createAppearanceTab(self):
        """Creates the 'Appearance' settings tab."""
        tab = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout(tab)
        
        self.themeCombo = QtWidgets.QComboBox()
        # List of example themes; adjust based on available qt-material themes.
        themes = ["dark_teal", "light_blue", "dark_blue", "dark_pink", "light"]
        self.themeCombo.addItems(themes)
        formLayout.addRow("Theme:", self.themeCombo)
        
        return tab

    def createAdvancedTab(self):
        """Creates the 'Advanced' settings tab."""
        tab = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout(tab)
        
        self.logLevelCombo = QtWidgets.QComboBox()
        log_levels = ["Error", "Warning", "Info", "Debug"]
        self.logLevelCombo.addItems(log_levels)
        formLayout.addRow("Log Level:", self.logLevelCombo)
        
        self.enableDebugCheckbox = QtWidgets.QCheckBox("Enable Debug Mode")
        formLayout.addRow("Debug Mode:", self.enableDebugCheckbox)
        
        return tab

    def loadSettingsIntoUI(self):
        """Load settings from the Settings object into the dialog's UI controls."""
        # General tab
        self.autoSaveCheckbox.setChecked(self.settings.get_option("auto_save", True))
        self.showNotificationsCheckbox.setChecked(self.settings.get_option("show_notifications", True))
        self.lastOpenedFileEdit.setText(self.settings.get_option("last_opened_file", ""))
        self.recentFilesList.clear()
        for file in self.settings.get_option("recent_files", []):
            self.recentFilesList.addItem(file)
        
        # Appearance tab
        current_theme = self.settings.get_option("theme", "dark_teal")
        index = self.themeCombo.findText(current_theme)
        if index >= 0:
            self.themeCombo.setCurrentIndex(index)
        
        # Advanced tab
        current_log_level = self.settings.get_option("log_level", "Info")
        index = self.logLevelCombo.findText(current_log_level)
        if index >= 0:
            self.logLevelCombo.setCurrentIndex(index)
        self.enableDebugCheckbox.setChecked(self.settings.get_option("debug_mode", False))

    def applySettings(self):
        """Apply the changes made in the dialog back to the Settings object."""
        self.settings.set_option("auto_save", self.autoSaveCheckbox.isChecked())
        self.settings.set_option("show_notifications", self.showNotificationsCheckbox.isChecked())
        self.settings.set_option("theme", self.themeCombo.currentText())
        self.settings.set_option("log_level", self.logLevelCombo.currentText())
        self.settings.set_option("debug_mode", self.enableDebugCheckbox.isChecked())
        # Note: 'last_opened_file' and 'recent_files' are read-only here.
        self.accept()

    def resetDefaults(self):
        """Reset all settings to default values and update the UI."""
        reply = QtWidgets.QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset settings to defaults?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.settings.reset_to_defaults()
            self.loadSettingsIntoUI()

# Quick standalone test for settings.py functionality.
if __name__ == "__main__":
    import sys
    from qt_material import apply_stylesheet

    app = QtWidgets.QApplication(sys.argv)
    # Apply a qt-material theme – make sure the theme file is available.
    apply_stylesheet(app, theme='dark_teal.xml')

    settings = Settings()
    dlg = SettingsDialog(settings)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
        print("Updated Settings:")
        print(json.dumps(settings.options, indent=4))
    else:
        print("Settings update canceled.")
    sys.exit(0)
