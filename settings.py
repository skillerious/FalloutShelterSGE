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
            "debug_mode": False,
            # Backup options:
            "auto_backup": False,
            "backup_on_load": False,
            "backup_folder": os.path.join(os.path.expanduser("~"), "BackupSave"),
            "backup_frequency": 10,        # in minutes
            "append_timestamp": True,      # whether to append timestamp to backup file name
            "max_backup_files": 5,         # maximum backup files to keep
            # Misc options:
            "default_open_folder": os.path.expanduser("~"),
            "language": "English",
            "font_size": 12
        }
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
        self.resize(700, 500)
        self.initUI()

    def initUI(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Create a QTabWidget to hold different settings categories
        self.tabWidget = QtWidgets.QTabWidget()
        mainLayout.addWidget(self.tabWidget)

        # Create individual tabs: General, Appearance, Advanced, Backup, Misc
        self.generalTab = self.createGeneralTab()
        self.appearanceTab = self.createAppearanceTab()
        self.advancedTab = self.createAdvancedTab()
        self.backupTab = self.createBackupTab()
        self.miscTab = self.createMiscTab()

        self.tabWidget.addTab(self.generalTab, "General")
        self.tabWidget.addTab(self.appearanceTab, "Appearance")
        self.tabWidget.addTab(self.advancedTab, "Advanced")
        self.tabWidget.addTab(self.backupTab, "Backup")
        self.tabWidget.addTab(self.miscTab, "Misc")

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
        # Example themes; adjust based on available qt-material themes.
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

    def createBackupTab(self):
        """Creates the 'Backup' settings tab."""
        tab = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout(tab)
        
        self.autoBackupCheckbox = QtWidgets.QCheckBox("Enable Automatic Backup")
        formLayout.addRow("Auto Backup:", self.autoBackupCheckbox)
        
        self.backupOnLoadCheckbox = QtWidgets.QCheckBox("Backup on File Load")
        formLayout.addRow("Backup on Load:", self.backupOnLoadCheckbox)
        
        self.backupFrequencySpin = QtWidgets.QSpinBox()
        self.backupFrequencySpin.setRange(1, 1440)
        formLayout.addRow("Backup Frequency (min):", self.backupFrequencySpin)
        
        self.appendTimestampCheckbox = QtWidgets.QCheckBox("Append Timestamp to Backup Filename")
        formLayout.addRow("Append Timestamp:", self.appendTimestampCheckbox)
        
        self.maxBackupFilesSpin = QtWidgets.QSpinBox()
        self.maxBackupFilesSpin.setRange(1, 100)
        formLayout.addRow("Max Backup Files:", self.maxBackupFilesSpin)
        
        self.backupFolderEdit = QtWidgets.QLineEdit()
        default_folder = self.settings.get_option("default_open_folder", os.path.expanduser("~"))
        self.backupFolderEdit.setText(os.path.join(default_folder, "BackupSave"))
        backupFolderButton = QtWidgets.QPushButton("Browse")
        backupFolderButton.clicked.connect(self.browseBackupFolder)
        folderLayout = QtWidgets.QHBoxLayout()
        folderLayout.addWidget(self.backupFolderEdit)
        folderLayout.addWidget(backupFolderButton)
        formLayout.addRow("Backup Folder:", folderLayout)
        
        return tab

    def createMiscTab(self):
        """Creates the 'Misc' settings tab."""
        tab = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout(tab)
        
        self.defaultOpenFolderEdit = QtWidgets.QLineEdit()
        self.defaultOpenFolderEdit.setText(self.settings.get_option("default_open_folder", os.path.expanduser("~")))
        defaultFolderButton = QtWidgets.QPushButton("Browse")
        defaultFolderButton.clicked.connect(self.browseDefaultFolder)
        folderLayout = QtWidgets.QHBoxLayout()
        folderLayout.addWidget(self.defaultOpenFolderEdit)
        folderLayout.addWidget(defaultFolderButton)
        formLayout.addRow("Default Open Folder:", folderLayout)
        
        self.languageCombo = QtWidgets.QComboBox()
        languages = ["English", "Spanish", "French", "German", "Chinese"]
        self.languageCombo.addItems(languages)
        formLayout.addRow("Language:", self.languageCombo)
        
        self.fontSizeSpin = QtWidgets.QSpinBox()
        self.fontSizeSpin.setRange(8, 32)
        formLayout.addRow("Font Size:", self.fontSizeSpin)
        
        return tab

    def browseBackupFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Backup Folder", self.backupFolderEdit.text())
        if folder:
            self.backupFolderEdit.setText(folder)

    def browseDefaultFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Default Open Folder", self.defaultOpenFolderEdit.text())
        if folder:
            self.defaultOpenFolderEdit.setText(folder)

    def loadSettingsIntoUI(self):
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
        
        # Backup tab
        self.autoBackupCheckbox.setChecked(self.settings.get_option("auto_backup", False))
        self.backupOnLoadCheckbox.setChecked(self.settings.get_option("backup_on_load", False))
        self.backupFrequencySpin.setValue(self.settings.get_option("backup_frequency", 10))
        self.appendTimestampCheckbox.setChecked(self.settings.get_option("append_timestamp", True))
        self.maxBackupFilesSpin.setValue(self.settings.get_option("max_backup_files", 5))
        self.backupFolderEdit.setText(self.settings.get_option("backup_folder", os.path.join(self.settings.get_option("default_open_folder", os.path.expanduser("~")), "BackupSave")))
        
        # Misc tab
        self.defaultOpenFolderEdit.setText(self.settings.get_option("default_open_folder", os.path.expanduser("~")))
        current_language = self.settings.get_option("language", "English")
        index = self.languageCombo.findText(current_language)
        if index >= 0:
            self.languageCombo.setCurrentIndex(index)
        self.fontSizeSpin.setValue(self.settings.get_option("font_size", 12))

    def applySettings(self):
        # General tab
        self.settings.set_option("auto_save", self.autoSaveCheckbox.isChecked())
        self.settings.set_option("show_notifications", self.showNotificationsCheckbox.isChecked())
        self.settings.set_option("theme", self.themeCombo.currentText())
        # Advanced tab
        self.settings.set_option("log_level", self.logLevelCombo.currentText())
        self.settings.set_option("debug_mode", self.enableDebugCheckbox.isChecked())
        # Backup tab
        self.settings.set_option("auto_backup", self.autoBackupCheckbox.isChecked())
        self.settings.set_option("backup_on_load", self.backupOnLoadCheckbox.isChecked())
        self.settings.set_option("backup_frequency", self.backupFrequencySpin.value())
        self.settings.set_option("append_timestamp", self.appendTimestampCheckbox.isChecked())
        self.settings.set_option("max_backup_files", self.maxBackupFilesSpin.value())
        self.settings.set_option("backup_folder", self.backupFolderEdit.text())
        # Misc tab
        self.settings.set_option("default_open_folder", self.defaultOpenFolderEdit.text())
        self.settings.set_option("language", self.languageCombo.currentText())
        self.settings.set_option("font_size", self.fontSizeSpin.value())
        self.accept()

    def resetDefaults(self):
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
    apply_stylesheet(app, theme='dark_teal.xml')
    settings = Settings()
    dlg = SettingsDialog(settings)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
        print("Updated Settings:")
        print(json.dumps(settings.options, indent=4))
    else:
        print("Settings update canceled.")
    sys.exit(0)
