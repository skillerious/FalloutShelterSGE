# Fallout Shelter Save Editor

![Fallout Shelter Save Editor](assets/banner.png)

A comprehensive save editor for **Fallout Shelter**, built with **Python**, **PyQt5**, and **qt-material**. This editor is inspired by the [online save editor](https://rakion99.github.io/shelter-editor/) and brings a **desktop-based** alternative with an enhanced user interface and additional features.

⚠ **Use at Your Own Risk:** Modifying game save files can lead to unexpected behavior. Always back up your original save before making changes.

---

## 🚀 Features

### 🏠 Vault Management
- Edit vault resources (caps, nuka cola, food, water, energy, etc.)
- Modify vault name, population, XP, score, happiness
- Unlock all rooms and themes
- Remove all rocks
- Maximize all dweller stats and happiness

### 👥 Dwellers Editing
- Modify dweller names, gender, and appearance
- Edit health, radiation, level, XP, happiness
- Customize equipped weapons and outfits
- Change SPECIAL stats (Strength, Perception, Endurance, etc.)
- Mark dwellers as pregnant or ready for childbirth

### 🌍 Wasteland Exploration
- Modify exploration teams
- Adjust time spent exploring and return duration
- Change team resources (stim packs, radaway, caps, nuka cola)

### 🏗️ Room Editing
- Modify rooms and their current state
- Change production progress
- Unlock all rooms instantly

### 🔧 Advanced Features
- Raw JSON editor for full customization
- Backup and restore save files
- Encryption & decryption of save data

### 🎨 User Settings & Customization
- **Theme selection**: Supports `dark_teal`, `light_blue`, `dark_pink`, and more
- **Auto-save**: Toggle automatic save on exit
- **Notifications**: Enable or disable in-app notifications
- **Debug mode**: Useful for advanced users

---

## 🛠 Installation

### Requirements
- **Python 3.8+**
- **pip** package manager
- **Fallout Shelter** (PC/Steam/Microsoft Store/Android/iOS)

### Clone Repository
```sh
git clone https://github.com/your-username/FalloutShelterSaveEditor.git
cd FalloutShelterSaveEditor
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Run the Editor
```sh
python main.py
```

---

## 📂 Save File Locations

| Platform        | Save Location |
|----------------|--------------|
| **PC (Bethesda Launcher)** | `~/Documents/My Games/Fallout Shelter/` |
| **Steam (PC)** | `~/AppData/Local/FalloutShelter/` |
| **Windows 10 Store** | `C:\Users\YourName\AppData\Local\Packages\BethesdaSoftworks.FalloutShelter_SystemAppData\wgs\...` |
| **Android** | `/storage/emulated/0/Android/data/com.bethsoft.falloutshelter/files` |
| **iOS** | Requires iTunes backup + external tools (iExplorer/iMazing) |

💡 **Tip:** Back up your save files before making changes!

---

## 📜 Usage Guide

1. **Open Fallout Shelter Save Editor**
2. **Load your save file** (`.sav`)
3. **Make edits** using the Vault, Dwellers, Wasteland, or Rooms tabs
4. **Apply changes** and save
5. **Launch Fallout Shelter and enjoy your modified vault!**

---

## ⚙️ Settings & Customization

Settings are stored in:
- **Windows:** `%APPDATA%/FalloutShelterSaveEditor/settings.json`
- **Mac/Linux:** `~/FalloutShelterSaveEditor/settings.json`

To reset settings, delete the `settings.json` file.

---

## 💡 Troubleshooting

### ❌ Save file not found?
- Ensure **Fallout Shelter is installed**
- Check the **save file location** listed above
- Some platforms use **hidden folders** (enable hidden files in File Explorer)

### 🔄 Changes not applying?
- **Close Fallout Shelter** before editing
- Ensure you **saved changes** before exiting the editor
- Check if **Cloud Sync** (Steam/Xbox) is overwriting your changes

### ⚠️ Corrupted Save?
- Restore from a **backup**
- Use the **Advanced JSON Editor** to fix any errors
- Start with small changes and test before making large modifications

---

## 🖼 Screenshots

**Vault Management Interface:**
![Vault Management](assets/vault-tab.png)

**Dwellers Editing:**
![Dwellers Editing](assets/dwellers-tab.png)

**Advanced JSON Editor:**
![JSON Editor](assets/json-editor.png)

---

## 🛠 Development

### Contributing
Pull requests are welcome! Feel free to submit bug reports or feature requests.

1. **Fork the repository**
2. **Create a new branch**
3. **Make your changes**
4. **Submit a pull request**

### Planned Features 🚀
- Auto-detect save files
- More advanced dweller customization
- Steam/Xbox Cloud Sync override
- Dark mode UI improvements

---

## ⚠ Disclaimer
This project is intended for **educational purposes** only. Modifying game files can lead to unintended consequences, including corrupted saves. **Use at your own risk** and always keep backups.

The Fallout Shelter game and its assets are owned by **Bethesda Softworks**. This project is not affiliated with or endorsed by Bethesda.

---

## 📜 License
MIT License. See `LICENSE` for details.

---

## 📢 Credits
Developed with ❤️ by **Robin Doak** and contributors.
