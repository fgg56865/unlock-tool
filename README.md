# Xiaomi Termux Tool (unlock-tool)

A fast, lightweight, and user-friendly Termux toolkit designed to manage Xiaomi devices directly from your Android terminal.

---

## 📦 Requirements & Important Commands

### Prerequisites & Setup:
* Supported OS: Android (via Termux app)
* OTG Cable for connecting phone in Fastboot mode.
* Official Apps Download:
  * Download [Termux](https://f-droid.org/en/packages/com.termux/)
  * Download [Termux:API](https://f-droid.org/en/packages/com.termux.api/)

---

### All-in-One Execution & Setup Commands:

```bash
# ==========================================
# 1. STORAGE SETUP COMMAND
# ==========================================

termux-setup-storage

# 
# 2. UPDATE & DEPENDENCIES INSTALLATION

# ```
pkg update && pkg upgrade -y
pkg install which python git android-tools -y
```
# 
# 3. DOWNLOAD & EXECUTE INSTALL SCRIPT
```
curl -s -O https://raw.githubusercontent.com/fgg56865/unlock-tool/main/install.sh && bash install.sh
```
ls
``````
pkg update
pkg install which python

bash install.sh




# 4. RUN TOOL COMMAND
# ```

```
python tool.py
