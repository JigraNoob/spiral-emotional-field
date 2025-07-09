# Spiral Environment Guide

This guide helps you navigate the Spiral project across different terminal environments: Git Bash, WSL, and PowerShell.

## 🌬️ **Environment Detection**

The Spiral setup automatically detects your environment:

- **🪟 Git Bash** (MINGW64): Unix-like shell on Windows
- **🐧 WSL**: Windows Subsystem for Linux
- **🪟 PowerShell**: Windows native shell

## 🚀 **Quick Start for Each Environment**

### Git Bash (MINGW64) - Your Current Environment

```bash
# In Git Bash terminal:
chmod +x spiral_venv_realign.sh
./spiral_venv_realign.sh

# Or activate manually:
source ./swe-1/Scripts/activate
```

### WSL

```bash
# In WSL terminal:
chmod +x spiral_venv_realign.sh
./spiral_venv_realign.sh

# Or use direnv (if installed):
direnv allow
```

### PowerShell

```powershell
# In PowerShell:
.\spiral_venv_realign.ps1

# Or activate manually:
.\swe-1\Scripts\Activate.ps1
```

## 🔧 **Environment-Specific Details**

### Git Bash (MINGW64)

- **Virtual Environment Path**: `./swe-1/Scripts/`
- **Activation Script**: `./swe-1/Scripts/activate`
- **Python Path**: Uses Windows Python installation
- **File System**: Windows paths with Unix-style commands

### WSL

- **Virtual Environment Path**: `./swe-1/bin/`
- **Activation Script**: `./swe-1/bin/activate`
- **Python Path**: Linux Python installation
- **File System**: Linux paths, mounted Windows drives at `/mnt/c/`

### PowerShell

- **Virtual Environment Path**: `.\swe-1\Scripts\`
- **Activation Script**: `.\swe-1\Scripts\Activate.ps1`
- **Python Path**: Windows Python installation
- **File System**: Windows paths with PowerShell commands

## 🛠️ **Troubleshooting**

### Cross-Platform Virtual Environment Issues

If you get "activation script missing" errors:

1. **Delete and recreate the venv**:

   ```bash
   # Git Bash/WSL
   rm -rf swe-1
   python -m venv swe-1

   # PowerShell
   Remove-Item -Recurse -Force swe-1
   python -m venv swe-1
   ```

2. **Use the alignment script**:

   ```bash
   # Git Bash/WSL
   ./spiral_venv_realign.sh

   # PowerShell
   .\spiral_venv_realign.ps1
   ```

### Python Path Issues

- **Git Bash**: Uses Windows Python, check `which python`
- **WSL**: Uses Linux Python, check `which python3`
- **PowerShell**: Uses Windows Python, check `Get-Command python`

### File Path Issues

- **Git Bash**: `/c/spiral` (Unix-style Windows paths)
- **WSL**: `/mnt/c/spiral` (Linux-style mounted paths)
- **PowerShell**: `C:\spiral` (Windows native paths)

## 🎯 **Recommended Workflow**

### For Development (Git Bash)

```bash
# 1. Open Git Bash in project directory
cd /c/spiral

# 2. Align environment
./spiral_venv_realign.sh

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
python -m pytest tests/

# 5. Start development
python your_script.py
```

### For Production (WSL)

```bash
# 1. Open WSL terminal
cd /mnt/c/spiral

# 2. Align environment
./spiral_venv_realign.sh

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run with direnv auto-activation
direnv allow
cd .  # Re-enter to trigger activation
```

## 🔄 **Environment Switching**

### From Git Bash to WSL

```bash
# In Git Bash
wsl

# In WSL
cd /mnt/c/spiral
./spiral_venv_realign.sh
```

### From PowerShell to Git Bash

```powershell
# In PowerShell
bash

# In Git Bash
cd /c/spiral
./spiral_venv_realign.sh
```

## 📁 **File Structure**

```
spiral/
├── .envrc                    # Multi-platform direnv config
├── spiral_venv_realign.sh    # Git Bash/WSL alignment
├── spiral_venv_realign.ps1   # PowerShell alignment
├── setup_wsl_env.sh          # WSL setup script
├── setup_windows_env.ps1     # Windows setup script
├── fix_venv_wsl.sh           # WSL venv fix script
├── swe-1/                    # Virtual environment
│   ├── Scripts/              # Windows activation scripts
│   ├── bin/                  # Linux activation scripts
│   └── ...
└── ...
```

## 🎨 **Cursor Integration**

### Python Interpreter Selection

1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose from your active virtual environment:
   - **Git Bash**: `./swe-1/Scripts/python.exe`
   - **WSL**: `./swe-1/bin/python`
   - **PowerShell**: `.\swe-1\Scripts\python.exe`

### Terminal Integration

- **Git Bash**: Use Git Bash terminal in Cursor
- **WSL**: Use WSL terminal in Cursor
- **PowerShell**: Use PowerShell terminal in Cursor

## 🌟 **Best Practices**

1. **Stick to one environment** per development session
2. **Use alignment scripts** when switching environments
3. **Keep virtual environment** in project root
4. **Use absolute imports** in Python code
5. **Run tests from project root** with `python -m pytest tests/`

## 🔮 **Advanced: Docker Integration**

For consistent environments across all platforms:

```bash
# Build and run with Docker
docker-compose -f ritual-stack.yml up -d --build

# This provides a consistent environment regardless of host OS
```

---

**Remember**: The Spiral project is designed to work across all these environments. Choose the one that feels most natural for your workflow! 🌬️
