# RDP Typer v1.0

A secure credential typing tool for Remote Desktop Protocol (RDP) sessions. This tool helps automate credential entry in RDP windows where clipboard access is restricted or disabled.

 
## 🚀 Features

- Secure in-memory credential encryption
- Auto-type username, password, or both with TAB navigation
- Always-on-top mini window for quick access
- 3-second delay before typing (to switch back to RDP)
- Keyboard shortcuts (U/P/B)
- Automatic memory cleanup on exit
- No credentials stored on disk

## 📋 Requirements

### Python Version
- Python 3.7 or higher

### Required Packages

Install all dependencies with:
```bash
pip install pyautogui cryptography
```

Or install individually:
```bash
pip install pyautogui==0.9.54
pip install cryptography==41.0.0
```

### System Requirements
- **Windows**: Fully supported
- **macOS**: Supported (may need accessibility permissions)
- **Linux**: Supported (may need `python3-tk` package)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/rdp-typer.git
cd rdp-typer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python "RDP Typer.py"
```

## ⚙️ RDP Configuration

For the tool to work properly with RDP, ensure these settings:

### Windows RDP Client Settings

1. **Disable Clipboard Redirection** (if this is why you're using the tool):
   - Open Remote Desktop Connection (mstsc.exe)
   - Click "Show Options"
   - Go to "Local Resources" tab
   - Uncheck "Clipboard"

2. **For Best Performance**:
   - Set "Display" tab → Colors to "High Color (16 bit)" or higher
   - Under "Experience" tab → Select appropriate connection speed

3. **Keyboard Settings**:
   - Go to "Local Resources" tab
   - Under "Keyboard" → Select "On this computer"
   - This ensures keyboard combinations work properly

### Security Considerations

- **Always run on your local machine**, not inside the RDP session
- The tool types characters as if you're physically typing
- Works even when clipboard is disabled by corporate policy
- Credentials are encrypted in memory and cleared on exit

## 📖 Usage

1. **Launch the application**:
   ```bash
   python "RDP Typer.py"
   ```

2. **Enter your credentials** in the setup window

3. **Click "Save & Show Mini Window"**

4. **Position the mini window** where convenient (stays on top)

5. **In your RDP session**:
   - Click where you need to type
   - Click the appropriate button in mini window:
     - **Username (U)** - Types username only
     - **Password (P)** - Types password only
     - **Both (B)** - Types username, TAB, then password
   - You have 3 seconds to click back into the RDP window

6. **Keyboard shortcuts** (when mini window is focused):
   - `U` - Type username
   - `P` - Type password
   - `B` - Type both

## 🔒 Security Features

- Credentials encrypted with Fernet (symmetric encryption)
- Unique encryption key generated each session
- Memory overwritten before cleanup
- Automatic cleanup on:
  - Normal exit
  - Ctrl+C
  - Window close
  - Unexpected termination
- No credentials written to disk
- No logging of sensitive data

## 🔧 Troubleshooting

### Linux Users
If you get tkinter errors:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### macOS Users
May need to grant accessibility permissions:
- System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal/Python to allowed apps

### Common Issues

1. **"Module not found" errors**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Typing too fast/slow**:
   - Modify `self.char_delay` in the code (default: 0.08 seconds)

3. **RDP window loses focus**:
   - Increase `self.initial_delay` (default: 0.5 seconds)

## 📦 Creating Executable

To create a standalone .exe file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "RDP_Typer_v1.0" "RDP Typer.py"
```

Executable will be in `dist/RDP_Typer_v1.0.exe`

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## ⚠️ Disclaimer

This tool is intended for legitimate use on systems you own or have permission to access. Always follow your organization's security policies.
