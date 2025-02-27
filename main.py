#!/usr/bin/env python
import sys
import os
import json
import base64
import struct
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox, QComboBox, QPushButton, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QScrollArea, QToolBar, QPlainTextEdit, QGroupBox
)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from qt_material import apply_stylesheet

# Import additional modules: Information and Settings dialogs
from info import InformationDialog
from settings import Settings, SettingsDialog

# ============================================================
#  Encryption / Decryption Functions
# ============================================================
key_ints = [2815074099, 1725469378, 4039046167, 874293617,
            3063605751, 3133984764, 4097598161, 3620741625]
key = struct.pack('>8I', *key_ints)
iv = bytes.fromhex("7475383967656A693334307438397532")

def decrypt_sav(content):
    try:
        cipher_data = base64.b64decode(content)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plain = cipher.decrypt(cipher_data)
        try:
            plain = unpad(plain, AES.block_size)
        except ValueError:
            pass
        return plain.decode('utf-8')
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

def encrypt_sav(json_text):
    try:
        data = json_text.encode('utf-8')
        padded_data = pad(data, AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")

# ============================================================
#  Vault Tab Widget (with Advanced Vault Options)
# ============================================================
class VaultTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        form = QFormLayout()
        self.vaultNameSpin = QSpinBox(); self.vaultNameSpin.setRange(0, 999)
        form.addRow("Vault Name:", self.vaultNameSpin)
        self.capsSpin = QSpinBox(); self.capsSpin.setRange(0, 10**9)
        form.addRow("Caps:", self.capsSpin)
        self.nukaSpin = QSpinBox(); self.nukaSpin.setRange(0, 10**9)
        form.addRow("Nuka Cola Quantums:", self.nukaSpin)
        self.foodSpin = QSpinBox(); self.foodSpin.setRange(0, 10**9)
        form.addRow("Food:", self.foodSpin)
        self.energySpin = QSpinBox(); self.energySpin.setRange(0, 10**9)
        form.addRow("Energy:", self.energySpin)
        self.waterSpin = QSpinBox(); self.waterSpin.setRange(0, 10**9)
        form.addRow("Water:", self.waterSpin)
        self.stimpackSpin = QSpinBox(); self.stimpackSpin.setRange(0, 10**9)
        form.addRow("StimPack:", self.stimpackSpin)
        self.radawaySpin = QSpinBox(); self.radawaySpin.setRange(0, 10**9)
        form.addRow("RadAway:", self.radawaySpin)
        self.lunchboxSpin = QSpinBox(); self.lunchboxSpin.setRange(0, 1000)
        form.addRow("Lunch Boxes:", self.lunchboxSpin)
        self.handySpin = QSpinBox(); self.handySpin.setRange(0, 1000)
        form.addRow("Mr. Handies:", self.handySpin)
        self.petCarrierSpin = QSpinBox(); self.petCarrierSpin.setRange(0, 1000)
        form.addRow("Pet Carriers:", self.petCarrierSpin)
        self.starterPackSpin = QSpinBox(); self.starterPackSpin.setRange(0, 1000)
        form.addRow("Starter Packs:", self.starterPackSpin)
        self.modeCombo = QComboBox(); self.modeCombo.addItems(["Normal", "Survival"])
        form.addRow("Vault Mode:", self.modeCombo)
        self.themeCombo = QComboBox()
        self.themeCombo.addItem("Normal", 0)
        self.themeCombo.addItem("Xmas", 1)
        self.themeCombo.addItem("Halloween", 2)
        self.themeCombo.addItem("ThanksGiving", 3)
        form.addRow("Vault Theme:", self.themeCombo)
        mainLayout.addLayout(form)

        advGroup = QGroupBox("Advanced Vault Options")
        advForm = QFormLayout()
        self.xpSpin = QSpinBox(); self.xpSpin.setRange(0, 10**6)
        advForm.addRow("Vault XP:", self.xpSpin)
        self.populationSpin = QSpinBox(); self.populationSpin.setRange(0, 1000)
        advForm.addRow("Population:", self.populationSpin)
        self.happinessSpinVault = QSpinBox(); self.happinessSpinVault.setRange(0, 100)
        advForm.addRow("Happiness:", self.happinessSpinVault)
        self.scoreSpin = QSpinBox(); self.scoreSpin.setRange(0, 10**6)
        advForm.addRow("Score:", self.scoreSpin)
        advGroup.setLayout(advForm)
        mainLayout.addWidget(advGroup)

        cheatLayout = QHBoxLayout()
        btnRemoveRocks = QPushButton("Remove Rocks")
        btnRemoveRocks.clicked.connect(lambda: self.main_window.action_removeRocks())
        cheatLayout.addWidget(btnRemoveRocks)
        btnUnlockRooms = QPushButton("Unlock All Rooms")
        btnUnlockRooms.clicked.connect(lambda: self.main_window.action_unlockRooms())
        cheatLayout.addWidget(btnUnlockRooms)
        btnUnlockRecipes = QPushButton("Unlock All Recipes")
        btnUnlockRecipes.clicked.connect(lambda: self.main_window.action_unlockRecipes())
        cheatLayout.addWidget(btnUnlockRecipes)
        mainLayout.addLayout(cheatLayout)

        cheatLayout2 = QHBoxLayout()
        btnMaxStats = QPushButton("Max All Dweller Stats")
        btnMaxStats.clicked.connect(lambda: self.main_window.action_maxSpecialAll())
        cheatLayout2.addWidget(btnMaxStats)
        btnMaxHappiness = QPushButton("Max All Dweller Happiness")
        btnMaxHappiness.clicked.connect(lambda: self.main_window.action_maxHappinessAll())
        cheatLayout2.addWidget(btnMaxHappiness)
        btnHealAll = QPushButton("Heal All Dwellers")
        btnHealAll.clicked.connect(lambda: self.main_window.action_healAll())
        cheatLayout2.addWidget(btnHealAll)
        mainLayout.addLayout(cheatLayout2)

        cheatLayout3 = QHBoxLayout()
        btnClearEmergency = QPushButton("Clear Emergency")
        btnClearEmergency.clicked.connect(lambda: self.main_window.action_clearEmergency())
        cheatLayout3.addWidget(btnClearEmergency)
        btnAcceptWaiting = QPushButton("Accept Waiting Dwellers")
        btnAcceptWaiting.clicked.connect(lambda: self.main_window.action_acceptWaiting())
        cheatLayout3.addWidget(btnAcceptWaiting)
        btnUnlockThemes = QPushButton("Unlock Themes")
        btnUnlockThemes.clicked.connect(lambda: self.main_window.action_unlockThemes())
        cheatLayout3.addWidget(btnUnlockThemes)
        mainLayout.addLayout(cheatLayout3)

        self.versionLabel = QLabel("")
        mainLayout.addWidget(self.versionLabel)
        self.setLayout(mainLayout)
        
    def setData(self, data):
        vault = data.get("vault", {})
        try:
            self.vaultNameSpin.setValue(int(vault.get("VaultName", "0")))
        except:
            self.vaultNameSpin.setValue(0)
        resources = vault.get("storage", {}).get("resources", {})
        self.capsSpin.setValue(int(resources.get("Nuka", 0)))
        self.nukaSpin.setValue(int(resources.get("NukaColaQuantum", 0)))
        self.foodSpin.setValue(int(resources.get("Food", 0)))
        self.energySpin.setValue(int(resources.get("Energy", 0)))
        self.waterSpin.setValue(int(resources.get("Water", 0)))
        self.stimpackSpin.setValue(int(resources.get("StimPack", 0)))
        self.radawaySpin.setValue(int(resources.get("RadAway", 0)))
        lb = vault.get("LunchBoxesByType", [])
        self.lunchboxSpin.setValue(lb.count(0))
        self.handySpin.setValue(lb.count(1))
        self.petCarrierSpin.setValue(lb.count(2))
        self.starterPackSpin.setValue(lb.count(3))
        mode = vault.get("VaultMode", "Normal")
        idx = self.modeCombo.findText(mode)
        if idx >= 0: self.modeCombo.setCurrentIndex(idx)
        theme = vault.get("VaultTheme", 0)
        idx = self.themeCombo.findData(int(theme))
        if idx >= 0: self.themeCombo.setCurrentIndex(idx)
        self.xpSpin.setValue(int(vault.get("XP", 0)))
        self.populationSpin.setValue(int(vault.get("population", 0)))
        self.happinessSpinVault.setValue(int(vault.get("happiness", 0)))
        self.scoreSpin.setValue(int(vault.get("score", 0)))
        version = vault.get("appVersion", "1.0.0")
        self.versionLabel.setText("App Version: " + str(version))
        
    def updateData(self, data):
        if "vault" not in data: data["vault"] = {}
        vault = data["vault"]
        vault["VaultName"] = str(self.vaultNameSpin.value()).zfill(3)
        if "storage" not in vault: vault["storage"] = {}
        if "resources" not in vault["storage"]: vault["storage"]["resources"] = {}
        resources = vault["storage"]["resources"]
        resources["Nuka"] = self.capsSpin.value()
        resources["NukaColaQuantum"] = self.nukaSpin.value()
        resources["Food"] = self.foodSpin.value()
        resources["Energy"] = self.energySpin.value()
        resources["Water"] = self.waterSpin.value()
        resources["StimPack"] = self.stimpackSpin.value()
        resources["RadAway"] = self.radawaySpin.value()
        lb = ([0] * self.lunchboxSpin.value() +
              [1] * self.handySpin.value() +
              [2] * self.petCarrierSpin.value() +
              [3] * self.starterPackSpin.value())
        vault["LunchBoxesByType"] = lb
        vault["LunchBoxesCount"] = len(lb)
        vault["VaultMode"] = self.modeCombo.currentText()
        vault["VaultTheme"] = self.themeCombo.currentData()
        vault["XP"] = self.xpSpin.value()
        vault["population"] = self.populationSpin.value()
        vault["happiness"] = self.happinessSpinVault.value()
        vault["score"] = self.scoreSpin.value()

# ============================================================
#  Dwellers Tab Widget (with extra XP field)
# ============================================================
DWELLER_OUTFITS = {
    "VaultSuit": "Vault Suit",
    "BattleArmor": "Battle Armor",
    "PowerArmor": "Power Armor"
}
DWELLER_WEAPONS = {
    "Pistol": "10mm Pistol",
    "AssaultRifle": "Assault Rifle",
    "LaserPistol": "Laser Pistol"
}

class DwellersTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_dweller = None
        self.initUI()
        
    def initUI(self):
        mainLayout = QHBoxLayout()
        self.dwellerList = QListWidget()
        self.dwellerList.itemClicked.connect(self.onItemSelected)
        mainLayout.addWidget(self.dwellerList, 1)
        detailLayout = QFormLayout()
        self.firstNameEdit = QLineEdit(); detailLayout.addRow("First Name:", self.firstNameEdit)
        self.lastNameEdit = QLineEdit(); detailLayout.addRow("Last Name:", self.lastNameEdit)
        self.genderCombo = QComboBox()
        self.genderCombo.addItem("Female", 1)
        self.genderCombo.addItem("Male", 2)
        detailLayout.addRow("Gender:", self.genderCombo)
        self.happinessSpin = QSpinBox(); self.happinessSpin.setRange(0, 100)
        detailLayout.addRow("Happiness:", self.happinessSpin)
        self.healthSpin = QSpinBox(); self.healthSpin.setRange(0, 1000)
        detailLayout.addRow("Health:", self.healthSpin)
        self.maxHealthSpin = QSpinBox(); self.maxHealthSpin.setRange(0, 1000)
        detailLayout.addRow("Max Health:", self.maxHealthSpin)
        self.radiationSpin = QSpinBox(); self.radiationSpin.setRange(0, 1000)
        detailLayout.addRow("Radiation:", self.radiationSpin)
        self.levelSpin = QSpinBox(); self.levelSpin.setRange(1, 100)
        detailLayout.addRow("Level:", self.levelSpin)
        self.xpSpin = QSpinBox(); self.xpSpin.setRange(0, 10000)
        detailLayout.addRow("Experience:", self.xpSpin)
        self.skinColorEdit = QLineEdit(); detailLayout.addRow("Skin Color (Hex):", self.skinColorEdit)
        self.hairColorEdit = QLineEdit(); detailLayout.addRow("Hair Color (Hex):", self.hairColorEdit)
        self.pregnantCombo = QComboBox()
        self.pregnantCombo.addItem("Not Pregnant", False)
        self.pregnantCombo.addItem("Pregnant", True)
        detailLayout.addRow("Pregnant:", self.pregnantCombo)
        self.babyReadyCombo = QComboBox()
        self.babyReadyCombo.addItem("Not Ready", False)
        self.babyReadyCombo.addItem("Ready", True)
        detailLayout.addRow("Baby Ready:", self.babyReadyCombo)
        self.outfitCombo = QComboBox()
        for key, val in DWELLER_OUTFITS.items():
            self.outfitCombo.addItem(val, key)
        detailLayout.addRow("Equipped Outfit:", self.outfitCombo)
        self.weaponCombo = QComboBox()
        for key, val in DWELLER_WEAPONS.items():
            self.weaponCombo.addItem(val, key)
        detailLayout.addRow("Equipped Weapon:", self.weaponCombo)
        statsLayout = QHBoxLayout()
        self.statsSpins = []
        for label in ["S", "P", "E", "C", "I", "A", "L"]:
            spin = QSpinBox(); spin.setRange(0, 10); spin.setPrefix(label + ":")
            statsLayout.addWidget(spin); self.statsSpins.append(spin)
        detailLayout.addRow("SPECIAL:", statsLayout)
        self.btnMaxStats = QPushButton("Max Stats")
        self.btnMaxStats.clicked.connect(self.maxStats)
        detailLayout.addRow(self.btnMaxStats)
        detailWidget = QWidget(); detailWidget.setLayout(detailLayout)
        scroll = QScrollArea(); scroll.setWidget(detailWidget); scroll.setWidgetResizable(True)
        mainLayout.addWidget(scroll, 2)
        self.setLayout(mainLayout)
        
    def setData(self, dwellers):
        self.dwellerList.clear()
        self.dwellers = dwellers
        for d in dwellers:
            item = QListWidgetItem(d.get("name", "Unnamed") + " " + d.get("lastName", ""))
            item.setData(QtCore.Qt.UserRole, d)
            self.dwellerList.addItem(item)
            
    def onItemSelected(self, item):
        self.current_dweller = item.data(QtCore.Qt.UserRole)
        self.populateDetails(self.current_dweller)
        
    def populateDetails(self, d):
        self.firstNameEdit.setText(d.get("name", ""))
        self.lastNameEdit.setText(d.get("lastName", ""))
        idx = self.genderCombo.findData(d.get("gender", 2))
        if idx >= 0: self.genderCombo.setCurrentIndex(idx)
        self.happinessSpin.setValue(d.get("happiness", {}).get("happinessValue", 0))
        self.healthSpin.setValue(d.get("health", {}).get("healthValue", 0))
        self.maxHealthSpin.setValue(d.get("health", {}).get("maxHealth", 0))
        self.radiationSpin.setValue(d.get("health", {}).get("radiationValue", 0))
        self.levelSpin.setValue(d.get("experience", {}).get("currentLevel", 1))
        self.xpSpin.setValue(d.get("experience", {}).get("currentXP", 0))
        self.skinColorEdit.setText(str(d.get("skinColor", "")))
        self.hairColorEdit.setText(str(d.get("hairColor", "")))
        self.pregnantCombo.setCurrentIndex(0 if not d.get("pregnant", False) else 1)
        self.babyReadyCombo.setCurrentIndex(0 if not d.get("babyReady", False) else 1)
        idx = self.outfitCombo.findData(d.get("equipedOutfit", {}).get("id", ""))
        if idx >= 0: self.outfitCombo.setCurrentIndex(idx)
        idx = self.weaponCombo.findData(d.get("equipedWeapon", {}).get("id", ""))
        if idx >= 0: self.weaponCombo.setCurrentIndex(idx)
        stats = d.get("stats", {}).get("stats", [])
        for i in range(min(7, len(self.statsSpins))):
            self.statsSpins[i].setValue(stats[i].get("value", 0))
            
    def updateCurrentDweller(self):
        if not self.current_dweller: return
        d = self.current_dweller
        d["name"] = self.firstNameEdit.text()
        d["lastName"] = self.lastNameEdit.text()
        d["gender"] = self.genderCombo.currentData()
        d.setdefault("happiness", {})["happinessValue"] = self.happinessSpin.value()
        d.setdefault("health", {})["healthValue"] = self.healthSpin.value()
        d["health"]["maxHealth"] = self.maxHealthSpin.value()
        d["health"]["radiationValue"] = self.radiationSpin.value()
        d.setdefault("experience", {})["currentLevel"] = self.levelSpin.value()
        d["experience"]["currentXP"] = self.xpSpin.value()
        d["skinColor"] = self.skinColorEdit.text()
        d["hairColor"] = self.hairColorEdit.text()
        d["pregnant"] = self.pregnantCombo.currentData()
        d["babyReady"] = self.babyReadyCombo.currentData()
        d["equipedOutfit"] = {"id": self.outfitCombo.currentData()}
        d["equipedWeapon"] = {"id": self.weaponCombo.currentData()}
        stats = d.get("stats", {}).get("stats", [])
        for i in range(min(7, len(self.statsSpins))):
            if i < len(stats):
                stats[i]["value"] = self.statsSpins[i].value()
                
    def maxStats(self):
        if not self.current_dweller: return
        for spin in self.statsSpins:
            spin.setValue(10)
        self.updateCurrentDweller()

# ============================================================
#  Wasteland Teams Tab Widget
# ============================================================
class WastelandTeamEditor(QWidget):
    def __init__(self, team, is_actor=False):
        super().__init__()
        self.team = team; self.is_actor = is_actor
        self.initUI()
    def initUI(self):
        layout = QFormLayout()
        self.teamIndexLabel = QLabel("Team Index: " + str(self.team.get("teamIndex", "N/A")))
        layout.addRow(self.teamIndexLabel)
        self.timeSpentSpin = QSpinBox(); self.timeSpentSpin.setRange(0, 10**6)
        self.timeSpentSpin.setValue(self.team.get("elapsedTimeAliveExploring", 0))
        layout.addRow("Time Spent (sec):", self.timeSpentSpin)
        self.returnDurationSpin = QSpinBox(); self.returnDurationSpin.setRange(0, 10**6)
        self.returnDurationSpin.setValue(self.team.get("returnTripDuration", 0))
        layout.addRow("Return Duration (sec):", self.returnDurationSpin)
        equip = {}
        if self.is_actor:
            equip = self.team.get("actor", {}).get("equipment", {}).get("storage", {}).get("resources", {})
        else:
            equip = self.team.get("teamEquipment", {}).get("storage", {}).get("resources", {})
        self.stimSpin = QSpinBox(); self.stimSpin.setRange(0, 10**6)
        self.stimSpin.setValue(equip.get("StimPack", 0))
        layout.addRow("StimPack:", self.stimSpin)
        self.radSpin = QSpinBox(); self.radSpin.setRange(0, 10**6)
        self.radSpin.setValue(equip.get("RadAway", 0))
        layout.addRow("RadAway:", self.radSpin)
        self.capsSpin = QSpinBox(); self.capsSpin.setRange(0, 10**6)
        self.capsSpin.setValue(equip.get("Nuka", 0))
        layout.addRow("Caps:", self.capsSpin)
        self.nukaSpin = QSpinBox(); self.nukaSpin.setRange(0, 10**6)
        self.nukaSpin.setValue(equip.get("NukaColaQuantum", 0))
        layout.addRow("Nuka Cola Quantum:", self.nukaSpin)
        self.setLayout(layout)
    def updateTeam(self):
        self.team["elapsedTimeAliveExploring"] = self.timeSpentSpin.value()
        self.team["returnTripDuration"] = self.returnDurationSpin.value()
        resources = {
            "StimPack": self.stimSpin.value(),
            "RadAway": self.radSpin.value(),
            "Nuka": self.capsSpin.value(),
            "NukaColaQuantum": self.nukaSpin.value()
        }
        if self.is_actor:
            if "actor" in self.team and "equipment" in self.team["actor"]:
                self.team["actor"]["equipment"]["storage"]["resources"] = resources
        else:
            if "teamEquipment" in self.team:
                self.team["teamEquipment"]["storage"]["resources"] = resources

class WastelandTeamsTab(QWidget):
    def __init__(self, main_window, is_actor=False):
        super().__init__()
        self.main_window = main_window; self.is_actor = is_actor
        self.initUI()
    def initUI(self):
        layout = QHBoxLayout()
        self.teamList = QListWidget()
        self.teamList.itemClicked.connect(self.onTeamSelected)
        layout.addWidget(self.teamList, 1)
        self.editorArea = QScrollArea(); self.editorArea.setWidgetResizable(True)
        layout.addWidget(self.editorArea, 2)
        self.setLayout(layout)
        self.teams = []
    def setData(self, teams):
        self.teamList.clear()
        self.teams = teams
        for t in teams:
            name = t.get("actor", {}).get("name", "Unnamed") if self.is_actor else t.get("dweller", {}).get("name", "Unnamed")
            item = QListWidgetItem("Team " + str(t.get("teamIndex", "N/A")) + " - " + name)
            item.setData(QtCore.Qt.UserRole, t)
            self.teamList.addItem(item)
    def onTeamSelected(self, item):
        team = item.data(QtCore.Qt.UserRole)
        editor = WastelandTeamEditor(team, self.is_actor)
        self.editorArea.setWidget(editor)
        self.currentEditor = editor
    def updateCurrentTeam(self):
        if hasattr(self, "currentEditor"):
            self.currentEditor.updateTeam()

class WastelandTab(QTabWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.dwellerTab = WastelandTeamsTab(main_window, is_actor=False)
        self.actorTab = WastelandTeamsTab(main_window, is_actor=True)
        self.addTab(self.dwellerTab, "Dweller Teams")
        self.addTab(self.actorTab, "Actor Teams")
    def setData(self, data):
        teams = data.get("vault", {}).get("wasteland", {}).get("teams", [])
        dweller_teams = [t for t in teams if "dweller" in t]
        actor_teams = [t for t in teams if "actor" in t]
        self.dwellerTab.setData(dweller_teams)
        self.actorTab.setData(actor_teams)
    def updateData(self):
        self.dwellerTab.updateCurrentTeam()
        self.actorTab.updateCurrentTeam()

# ============================================================
#  Rooms Tab Widget
# ============================================================
class RoomsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QHBoxLayout()
        self.roomList = QListWidget()
        self.roomList.itemClicked.connect(self.onRoomSelected)
        layout.addWidget(self.roomList, 1)
        self.editorArea = QScrollArea(); self.editorArea.setWidgetResizable(True)
        layout.addWidget(self.editorArea, 2)
        self.setLayout(layout)
    def setData(self, rooms):
        self.roomList.clear()
        self.rooms = rooms
        for i, room in enumerate(rooms):
            text = f"Room {i+1}: {room.get('RoomType', 'Unknown')}"
            item = QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, (i, room))
            self.roomList.addItem(item)
    def onRoomSelected(self, item):
        idx, room = item.data(QtCore.Qt.UserRole)
        editor = RoomEditor(idx, room)
        self.editorArea.setWidget(editor)
        self.currentEditor = editor
    def updateData(self):
        if hasattr(self, "currentEditor"):
            self.currentEditor.updateRoom()

class RoomEditor(QWidget):
    def __init__(self, idx, room):
        super().__init__()
        self.idx = idx; self.room = room
        self.initUI()
    def initUI(self):
        layout = QFormLayout()
        self.roomTypeEdit = QLineEdit(str(self.room.get("RoomType", "")))
        layout.addRow("Room Type:", self.roomTypeEdit)
        self.stateEdit = QLineEdit(str(self.room.get("currentStateName", "")))
        layout.addRow("Current State:", self.stateEdit)
        self.progressSpin = QSpinBox(); self.progressSpin.setRange(0, 100)
        self.progressSpin.setValue(self.room.get("progress", 0))
        layout.addRow("Progress (%):", self.progressSpin)
        btnUpdate = QPushButton("Apply Changes")
        btnUpdate.clicked.connect(self.updateRoom)
        layout.addRow(btnUpdate)
        self.setLayout(layout)
    def updateRoom(self):
        self.room["RoomType"] = self.roomTypeEdit.text()
        self.room["currentStateName"] = self.stateEdit.text()
        self.room["progress"] = self.progressSpin.value()
        QMessageBox.information(self, "Room Updated", f"Room {self.idx+1} updated.")

# ============================================================
#  Advanced Tab (Raw JSON Editor)
# ============================================================
class AdvancedTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        self.rawEditor = QPlainTextEdit()
        layout.addWidget(self.rawEditor)
        btnApply = QPushButton("Apply Raw JSON Changes")
        btnApply.clicked.connect(self.applyChanges)
        layout.addWidget(btnApply)
        self.setLayout(layout)
    def setData(self, data):
        self.rawEditor.setPlainText(json.dumps(data, indent=4))
    def applyChanges(self):
        try:
            newData = json.loads(self.rawEditor.toPlainText())
            self.main_window.save_data = newData
            self.main_window.vaultTab.setData(newData)
            dwellers = newData.get("dwellers", {}).get("dwellers", [])
            self.main_window.dwellerTab.setData(dwellers)
            self.main_window.wastelandTab.setData(newData)
            if "rooms" in newData.get("vault", {}):
                self.main_window.roomsTab.setData(newData["vault"]["rooms"])
            QMessageBox.information(self, "Advanced", "Raw JSON changes applied.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON: {str(e)}")

# ============================================================
#  Main Application Window with Toolbar, Menu, and Status Bar
# ============================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fallout Shelter Save Editor")
        self.resize(1200, 900)
        self.save_data = None
        
        # Create our global settings instance and load settings
        self.app_settings = Settings()
        
        self.initUI()
        
    def initUI(self):
        self.createToolBar()
        self.tabs = QTabWidget()
        self.vaultTab = VaultTab(self)
        self.dwellerTab = DwellersTab(self)
        self.wastelandTab = WastelandTab(self)
        self.roomsTab = RoomsTab()
        self.advancedTab = AdvancedTab(self)
        self.tabs.addTab(self.vaultTab, "Vault")
        self.tabs.addTab(self.dwellerTab, "Dwellers")
        self.tabs.addTab(self.wastelandTab, "Wasteland")
        self.tabs.addTab(self.roomsTab, "Rooms")
        self.tabs.addTab(self.advancedTab, "Advanced")
        self.setCentralWidget(self.tabs)
        self.createMenuBar()
        self.setupStatusBar()
        self.statusMsgLabel.setText("Ready")
        
    def createToolBar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        openIcon = QtGui.QIcon("assets/open.png")
        saveIcon = QtGui.QIcon("assets/save.png")
        aboutIcon = QtGui.QIcon("assets/about.png")
        infoIcon = QtGui.QIcon("assets/info.png")
        settingsIcon = QtGui.QIcon("assets/settings.png")
        
        openAction = QtWidgets.QAction(openIcon, "Open", self)
        openAction.triggered.connect(self.open_file)
        toolbar.addAction(openAction)
        
        saveAction = QtWidgets.QAction(saveIcon, "Save", self)
        saveAction.triggered.connect(self.save_file)
        toolbar.addAction(saveAction)
        
        aboutAction = QtWidgets.QAction(aboutIcon, "About", self)
        aboutAction.triggered.connect(self.about)
        toolbar.addAction(aboutAction)
        
        infoAction = QtWidgets.QAction(infoIcon, "Information", self)
        infoAction.triggered.connect(self.information)
        toolbar.addAction(infoAction)
        
        settingsAction = QtWidgets.QAction(settingsIcon, "Settings", self)
        settingsAction.triggered.connect(self.open_settings)
        toolbar.addAction(settingsAction)
        
    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        openAct = QtWidgets.QAction("Open .sav", self)
        openAct.triggered.connect(self.open_file)
        fileMenu.addAction(openAct)
        saveAct = QtWidgets.QAction("Save .sav", self)
        saveAct.triggered.connect(self.save_file)
        fileMenu.addAction(saveAct)
        
        optionsMenu = menubar.addMenu("Options")
        settingsAct = QtWidgets.QAction("Settings", self)
        settingsAct.triggered.connect(self.open_settings)
        optionsMenu.addAction(settingsAct)
        
        helpMenu = menubar.addMenu("Help")
        aboutAct = QtWidgets.QAction("About", self)
        aboutAct.triggered.connect(self.about)
        helpMenu.addAction(aboutAct)
        infoAct = QtWidgets.QAction("Information", self)
        infoAct.triggered.connect(self.information)
        helpMenu.addAction(infoAct)
        
    def setupStatusBar(self):
        self.statusBar().clearMessage()
        self.versionStatusLabel = QtWidgets.QLabel("App Version: 1.0.0")
        self.statusMsgLabel = QtWidgets.QLabel("")
        self.statusMsgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusMsgLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.developerStatusLabel = QtWidgets.QLabel("Developed with <span style='color: red;'>❤️</span> by Robin Doak")
        self.developerStatusLabel.setTextFormat(QtCore.Qt.RichText)
        self.statusBar().addWidget(self.versionStatusLabel)
        self.statusBar().addWidget(self.statusMsgLabel, 1)
        self.statusBar().addPermanentWidget(self.developerStatusLabel)
        
    def about(self):
        QMessageBox.information(self, "About",
            "Fallout Shelter Save Editor\n\n"
            "A comprehensive editor for Fallout Shelter saves.\n"
            "Developed with PyQt5 and qt-material styling.\n\n"
            "Source code is available on GitHub.")
            
    def information(self):
        dlg = InformationDialog(self)
        dlg.exec_()
        
    def open_settings(self):
        dlg = SettingsDialog(self.app_settings, self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # Reapply theme based on updated settings
            from qt_material import apply_stylesheet
            app = QtWidgets.QApplication.instance()
            theme = self.app_settings.get_option("theme", "dark_teal")
            apply_stylesheet(app, theme=f"{theme}.xml")
            self.statusMsgLabel.setText("Settings updated and theme applied.")
        
    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open .sav File", "", "Save Files (*.sav);;All Files (*)")
        if fname:
            try:
                with open(fname, "r") as f:
                    content = f.read()
                json_text = decrypt_sav(content)
                self.save_data = json.loads(json_text)
                self.vaultTab.setData(self.save_data)
                dwellers = self.save_data.get("dwellers", {}).get("dwellers", [])
                self.dwellerTab.setData(dwellers)
                self.wastelandTab.setData(self.save_data)
                if "rooms" in self.save_data.get("vault", {}):
                    self.roomsTab.setData(self.save_data["vault"]["rooms"])
                self.advancedTab.setData(self.save_data)
                version = self.save_data.get("appVersion", "1.0.0")
                self.versionStatusLabel.setText("App Version: " + str(version))
                self.statusMsgLabel.setText("File loaded successfully")
                # Update settings with the last opened file and recent files list
                self.app_settings.set_option("last_opened_file", fname)
                recent = self.app_settings.get_option("recent_files", [])
                if fname not in recent:
                    recent.append(fname)
                    self.app_settings.set_option("recent_files", recent)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                
    def save_file(self):
        if not self.save_data:
            QMessageBox.warning(self, "No Data", "Please load a save file first.")
            return
        self.dwellerTab.updateCurrentDweller()
        self.vaultTab.updateData(self.save_data)
        self.wastelandTab.updateData()
        self.roomsTab.updateData()
        json_text = json.dumps(self.save_data, separators=(',', ':'))
        try:
            encrypted = encrypt_sav(json_text)
            fname, _ = QFileDialog.getSaveFileName(self, "Save .sav File", "", "Save Files (*.sav);;All Files (*)")
            if fname:
                with open(fname, "w") as f:
                    f.write(encrypted)
                self.statusMsgLabel.setText("Save file written successfully!")
            else:
                self.statusMsgLabel.setText("Save cancelled")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    # ----- Vault Action Functions -----
    def action_removeRocks(self):
        if self.save_data and "vault" in self.save_data:
            self.save_data["vault"]["rocks"] = []
            QMessageBox.information(self, "Action", "Rocks removed!")
    def action_unlockRooms(self):
        if self.save_data and "unlockableMgr" in self.save_data:
            self.save_data["unlockableMgr"]["objectivesInProgress"] = []
            self.save_data["unlockableMgr"]["completed"] = []
            self.save_data["unlockableMgr"]["claimed"] = [
                "StorageUnlock", "MedbayUnlock", "SciencelabUnlock", "OverseerUnlock",
                "RadioStationUnlock", "WeaponFactoryUnlock", "GymUnlock", "DojoUnlock",
                "ArmoryUnlock", "ClassUnlock", "OutfitFactoryUnlock", "CardioUnlock",
                "BarUnlock", "GameRoomUnlock", "BarberShopUnlock", "PowerPlantUnlock",
                "WaterroomUnlock", "HydroponicUnlock", "NukacolaUnlock", "DesignFactoryUnlock"
            ]
            QMessageBox.information(self, "Action", "All rooms unlocked!")
    def action_unlockRecipes(self):
        if self.save_data and "survivalW" in self.save_data:
            self.save_data["survivalW"]["recipes"] = [
                "Shotgun_Rusty", "Railgun", "LaserPistol_Focused", "PlasmaThrower_Boosted",
                "PlasmaThrower_Overcharged", "PipePistol_LittleBrother", "CombatShotgun_Hardened"
            ]
            QMessageBox.information(self, "Action", "Recipes unlocked!")
    def action_maxSpecialAll(self):
        if self.save_data and "dwellers" in self.save_data:
            for d in self.save_data["dwellers"].get("dwellers", []):
                if "stats" in d and "stats" in d["stats"]:
                    for stat in d["stats"]["stats"]:
                        stat["value"] = 10
            QMessageBox.information(self, "Action", "All dweller stats set to max!")
    def action_maxHappinessAll(self):
        if self.save_data and "dwellers" in self.save_data:
            for d in self.save_data["dwellers"].get("dwellers", []):
                if "happiness" in d:
                    d["happiness"]["happinessValue"] = 100
            QMessageBox.information(self, "Action", "All dweller happiness maxed!")
    def action_healAll(self):
        if self.save_data and "dwellers" in self.save_data:
            for d in self.save_data["dwellers"].get("dwellers", []):
                if "health" in d:
                    d["health"]["radiationValue"] = 0
                    d["health"]["healthValue"] = d["health"].get("maxHealth", 0)
            QMessageBox.information(self, "Action", "All dwellers healed!")
    def action_clearEmergency(self):
        if self.save_data and "vault" in self.save_data and "rooms" in self.save_data["vault"]:
            for room in self.save_data["vault"]["rooms"]:
                room["currentStateName"] = "Idle"
            QMessageBox.information(self, "Action", "Emergency cleared on all rooms!")
    def action_acceptWaiting(self):
        if self.save_data and "dwellerSpawner" in self.save_data:
            self.save_data["dwellerSpawner"]["dwellersWaiting"] = []
            QMessageBox.information(self, "Action", "All waiting dwellers accepted!")
    def action_unlockThemes(self):
        if self.save_data and "survivalW" in self.save_data and "collectedThemes" in self.save_data["survivalW"]:
            for theme in self.save_data["survivalW"]["collectedThemes"].get("themeList", []):
                if "extraData" in theme:
                    theme["extraData"]["partsCollectedCount"] = 9
                    theme["extraData"]["IsNew"] = True
            QMessageBox.information(self, "Action", "Themes unlocked!")

# ============================================================
#  Main Function – Using qt-material Theme
# ============================================================
def main():
    app = QtWidgets.QApplication(sys.argv)
    # Apply initial theme from settings
    settings_instance = Settings()
    theme = settings_instance.get_option("theme", "dark_teal")
    apply_stylesheet(app, theme=f"{theme}.xml")
    
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
