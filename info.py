# info.py
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

def folder_exists(path: str) -> bool:
    """Utility to check if a given folder path actually exists on this system."""
    return os.path.exists(path) and os.path.isdir(path)


class InformationDialog(QtWidgets.QDialog):
    """
    A comprehensive multi-tabbed dialog with an improved layout:
      - A large QTabWidget that fills the window
      - A single "Open Folder" button at the bottom, next to "Close"
      - The "Open Folder" button is enabled/disabled depending on the active tab
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fallout Shelter Save Editing - Information & Guide")
        self.resize(900, 700)  # Adjust initial size as you wish

        # Data describing each tab: title, text (HTML), optional folder path
        # Adjust or expand the text content as needed.
        self.tabs_data = [
            {
                "title": "Overview",
                "html": (
                    "<h1>Fallout Shelter Save Editing Overview</h1>"
                    "<p>This guide provides in-depth instructions for locating and editing Fallout Shelter save files "
                    "on various platforms (PC/Launcher, Windows 10 Store, Steam, Android, iOS). You'll also find tips "
                    "for backup & restore procedures, troubleshooting common issues, and best practices.</p>"
                    "<p>Select a tab for platform-specific info or see 'Backup & Restore', 'Troubleshooting', and "
                    "'FAQs & Best Practices' for more details.</p>"
                ),
                "folder": None
            },
            {
                "title": "PC/Launcher",
                "html": (
                    "<h2>PC (Bethesda Launcher/Standalone) Save Locations</h2>"
                    "<p>On PC with the Bethesda.net or standalone version, your save files typically reside in:</p>"
                    "<blockquote><code>~/Documents/My Games/Fallout Shelter</code></blockquote>"
                    "<p>Replace <code>~</code> with your actual user folder path (on Windows, it's <code>C:\\Users\\YourName</code>).</p>"
                    "<p>Inside you'll find <em>Vault1.sav</em>, <em>Vault2.sav</em>, etc. and their backups <em>.sav.bkp</em>. "
                    "Copy them elsewhere for backups or overwriting for restore. Always close the game first!</p>"
                ),
                "folder": os.path.join(os.path.expanduser("~"), "Documents", "My Games", "Fallout Shelter")
            },
            {
                "title": "Windows 10",
                "html": (
                    "<h2>Windows 10 Store Version</h2>"
                    "<p>Saves for the Microsoft Store version are stored in a hidden folder, something like:</p>"
                    "<blockquote><code>C:\\Users\\YourName\\AppData\\Local\\Packages\\"
                    "BethesdaSoftworks.FalloutShelter_<randomID>\\SystemAppData\\wgs\\...</code></blockquote>"
                    "<p>You'll see three files for each vault: two small (~1KB) plus one large (50-100KB) which lacks an extension. "
                    "That large file is your real vault. You may add <code>.sav</code> temporarily to edit it, then remove it again. "
                    "If Cloud Sync is on, do this process offline to avoid overwrites.</p>"
                ),
                "folder": None  # We won't attempt to open this path because it's unique per user
            },
            {
                "title": "Steam",
                "html": (
                    "<h2>Steam (PC) Save Location</h2>"
                    "<p>For the Steam version on Windows, your save folder is usually located at:</p>"
                    "<blockquote><code>~/AppData/Local/FalloutShelter</code></blockquote>"
                    "<p>Again, you'll see <em>VaultX.sav</em> and <em>VaultX.sav.bkp</em>. Copy them for backup, restore by "
                    "overwriting when the game is closed. Temporarily disable Steam Cloud if needed. After verifying, you can "
                    "re-enable cloud sync if you want.</p>"
                ),
                "folder": os.path.join(os.path.expanduser("~"), "AppData", "Local", "FalloutShelter")
            },
            {
                "title": "Android",
                "html": (
                    "<h2>Android Devices</h2>"
                    "<p>Typically located at:</p>"
                    "<blockquote><code>/storage/emulated/0/Android/data/com.bethsoft.falloutshelter/files</code></blockquote>"
                    "<p>On newer Android versions, you may need a special file explorer or connect via USB to see it. "
                    "Look for <em>Vault1.sav</em>, etc. Always exit the game first to avoid partial data. To restore, "
                    "overwrite the same slot before launching the game.</p>"
                ),
                "folder": None  # Typically not directly openable on Windows; user must connect phone or use MTP
            },
            {
                "title": "iOS",
                "html": (
                    "<h2>iOS Devices</h2>"
                    "<p>iOS keeps saves in the app sandbox. You can't directly browse them unless you use iTunes backup + a "
                    "tool like iExplorer or iMazing, or have a jailbroken device. On un-jailbroken iOS, the recommended approach "
                    "is to rely on iCloud or iTunes backups. You can extract <em>VaultX.sav</em> from an iTunes backup. "
                    "Restoring an edited save to an iOS device usually requires injecting it into the backup and restoring that "
                    "entire backup to your iPhone or iPad.</p>"
                ),
                "folder": None
            },
            {
                "title": "Backup & Restore",
                "html": (
                    "<h2>Backup & Restore Procedures</h2>"
                    "<p><strong>PC (Bethesda & Steam):</strong> Copy your .sav and .sav.bkp files to a separate folder. "
                    "To restore, overwrite them while the game is closed.</p>"
                    "<p><strong>Windows 10 Store:</strong> Copy the three files (two small, one large) from the WGS folder. "
                    "Restore by returning them offline, ensuring the large file name is exactly what the game expects.</p>"
                    "<p><strong>Android:</strong> Copy from <code>Android/data/com.bethsoft.falloutshelter/files</code>. "
                    "Restore by overwriting the same Vault#.sav before launching the game.</p>"
                    "<p><strong>iOS:</strong> Usually done via iTunes or iCloud backups. For local editing, use iExplorer or iMazing. "
                    "Restoring requires re-injecting to a backup or a jailbroken device for direct file placement.</p>"
                    "<p>Cross-platform transfers are possible by renaming the file extension as needed. Always back up first!</p>"
                ),
                "folder": None
            },
            {
                "title": "Troubleshooting",
                "html": (
                    "<h2>Troubleshooting Common Issues</h2>"
                    "<ul>"
                    "<li><strong>Save Corruption:</strong> Always fully close the game before editing or copying save files. Keep backups.</li>"
                    "<li><strong>Encryption/Decryption Errors:</strong> Make sure the tool you're using is consistent. A single missed step can result in a broken file.</li>"
                    "<li><strong>Cloud Sync Overwrites:</strong> Turn off Steam Cloud or go offline for Windows Store to prevent older files from re-syncing. Then pick the local file if prompted.</li>"
                    "<li><strong>Wrong Folder or Filename:</strong> Windows Store saves have no extension, iOS requires backups, etc. Double-check path and naming.</li>"
                    "<li><strong>Crashes or Strange Behavior:</strong> Possibly out-of-range stats or invalid items. Try smaller changes and re-check your JSON or use known item IDs only.</li>"
                    "</ul>"
                ),
                "folder": None
            },
            {
                "title": "FAQs & Best Practices",
                "html": (
                    "<h2>FAQs & Best Practices</h2>"
                    "<h3>Common Questions</h3>"
                    "<ul>"
                    "<li><strong>Cross-Platform Transfers?</strong> Yes, manually copy the VaultX.sav. Rename or remove extension as needed.</li>"
                    "<li><strong>Achievements or Bans?</strong> There's no ban for local editing. Achievements typically still unlock on Win10/Xbox.</li>"
                    "<li><strong>Editor Tools?</strong> Online or desktop-based tools exist for easy encryption/decryption. Use reputable sources.</li>"
                    "<li><strong>Cloud Conflicts?</strong> Turn off network/Steam Cloud to be safe. Then re-enable after verifying your local changes.</li>"
                    "<li><strong>Lost Save Recovery?</strong> If you have .bkp, rename it to .sav. If both are missing, check your backups or iCloud (iOS), or Recycle Bin (PC).</li>"
                    "</ul>"
                    "<h3>Best Practices</h3>"
                    "<ol>"
                    "<li><strong>Multiple backups!</strong> Keep them safe before major edits.</li>"
                    "<li><strong>Change small things & test.</strong> Helps isolate problems quickly.</li>"
                    "<li><strong>Use known stable editing tools.</strong> Avoid manual hex editing unless you fully understand the encryption.</li>"
                    "<li><strong>Stay within normal ranges.</strong> Overextending stats or resources can break the game.</li>"
                    "<li><strong>Preserve the fun.</strong> Over-cheating might ruin the challenge. Consider moderate edits only.</li>"
                    "</ol>"
                ),
                "folder": None
            }
        ]

        self.initLayout()

    def initLayout(self):
        """
        Creates a tab widget that displays text content and a bottom row
        with 'Open Folder' + 'Close' side by side. 'Open Folder' is enabled/disabled
        depending on the currently selected tab's folder path.
        """
        mainLayout = QtWidgets.QVBoxLayout(self)

        # Create QTabWidget that will hold the text for each platform
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        mainLayout.addWidget(self.tabWidget, 1)

        # We'll store references to textEdits so we can fill them
        self.textEdits = []

        # Populate each tab from self.tabs_data
        for i, tabInfo in enumerate(self.tabs_data):
            page = QtWidgets.QWidget()
            pageLayout = QtWidgets.QVBoxLayout(page)

            textEdit = QtWidgets.QTextEdit()
            textEdit.setReadOnly(True)
            textEdit.setHtml(tabInfo["html"])
            textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            pageLayout.addWidget(textEdit)
            self.textEdits.append(textEdit)

            self.tabWidget.addTab(page, tabInfo["title"])

        # Bottom button row
        bottomLayout = QtWidgets.QHBoxLayout()
        # "Open Folder" button
        self.openFolderBtn = QtWidgets.QPushButton("Open Folder")
        self.openFolderBtn.clicked.connect(self.onOpenFolder)
        bottomLayout.addWidget(self.openFolderBtn)

        bottomLayout.addStretch(1)

        # "Close" button
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.accept)
        bottomLayout.addWidget(closeBtn)

        mainLayout.addLayout(bottomLayout)

        # Connect tab change signal to update button
        self.tabWidget.currentChanged.connect(self.onTabChanged)
        # Initialize button state
        self.onTabChanged(0)

        self.setLayout(mainLayout)

    def onTabChanged(self, index: int):
        """
        Whenever the user switches tabs, we check if there's a valid folder path
        for that tab. If so, enable "Open Folder", else disable it.
        """
        if index < 0 or index >= len(self.tabs_data):
            return
        folder = self.tabs_data[index].get("folder")
        if folder and os.name == 'nt':
            # Windows only: check if folder exists
            if folder_exists(folder):
                self.openFolderBtn.setEnabled(True)
                self.openFolderBtn.setToolTip(f"Click to open: {folder}")
            else:
                self.openFolderBtn.setEnabled(False)
                self.openFolderBtn.setToolTip(f"Folder not found: {folder}")
        else:
            # No folder or not on Windows => disable
            self.openFolderBtn.setEnabled(False)
            if folder:
                self.openFolderBtn.setToolTip("Open Folder is only supported on Windows")
            else:
                self.openFolderBtn.setToolTip("This tab doesn't have a direct folder path")

    def onOpenFolder(self):
        """
        Attempt to open the folder for the current tab, if it exists.
        """
        index = self.tabWidget.currentIndex()
        if index < 0 or index >= len(self.tabs_data):
            return
        folder = self.tabs_data[index].get("folder")
        if folder and folder_exists(folder):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(folder))


# For standalone testing
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = InformationDialog()
    dialog.exec_()
