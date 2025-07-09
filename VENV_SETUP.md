# Virtual Environment Setup Guide

This guide helps you set up automatic virtual environment activation for the Spiral project in both WSL and Windows environments.

## Quick Start

### For WSL (Recommended)

```bash
# Run the setup script
chmod +x setup_wsl_env.sh
./setup_wsl_env.sh

# Restart your terminal or reload bashrc
source ~/.bashrc

# Navigate to project directory
cd /mnt/c/spiral

# Virtual environment should auto-activate!
```

### For Windows PowerShell

```powershell
# Run the setup script
.\setup_windows_env.ps1

# Activate manually when needed
.\activate_venv.ps1
```

## How It Works

### WSL Setup (`.envrc`)

- Uses `direnv` to automatically activate the virtual environment
- Detects WSL environment and provides helpful feedback
- Shows Python and pip paths when activated
- Provides clear error messages if something goes wrong

### Windows Setup (`activate_venv.ps1`)

- PowerShell script for manual activation
- Shows Python and pip paths when activated
- Can be run anytime you need the virtual environment

## File Structure

```
spiral/
├── .envrc                    # WSL auto-activation (direnv)
├── setup_wsl_env.sh          # WSL setup script
├── setup_windows_env.ps1     # Windows setup script
├── activate_venv.ps1         # Windows manual activation
├── swe-1/                    # Virtual environment directory
│   ├── bin/                  # Linux/WSL binaries
│   ├── Scripts/              # Windows binaries
│   └── ...
└── ...
```

## Troubleshooting

### WSL Issues

1. **direnv not found**: Run `sudo apt install direnv`
2. **Hook not working**: Add `eval "$(direnv hook bash)"` to `~/.bashrc`
3. **Permission denied**: Run `chmod +x setup_wsl_env.sh`

### Windows Issues

1. **Execution policy**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
2. **Python not found**: Install Python from python.org
3. **venv creation fails**: Try `python -m venv --clear swe-1`

### General Issues

1. **Recreate virtual environment**:

   - WSL: `rm -rf swe-1 && python3 -m venv swe-1 && direnv allow`
   - Windows: `Remove-Item -Recurse -Force swe-1; python -m venv swe-1`

2. **Check activation**:
   - WSL: `which python && which pip`
   - Windows: `Get-Command python | Select-Object Source`

## Environment Variables

The `.envrc` can be extended to include project-specific environment variables:

```bash
# Add to .envrc
export PYTHONPATH="$PWD:$PYTHONPATH"
export SPIRAL_ENV="development"
```

## Best Practices

1. **Always use the virtual environment** for development
2. **Keep requirements.txt updated** with `pip freeze > requirements.txt`
3. **Use absolute imports** in your Python code (as per project preferences)
4. **Run tests from project root** with `python -m pytest tests/`

## Commands Reference

### WSL

```bash
# Activate manually (if direnv fails)
source swe-1/bin/activate

# Deactivate
deactivate

# Install packages
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Windows

```powershell
# Activate manually
.\swe-1\Scripts\Activate.ps1

# Deactivate
deactivate

# Install packages
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```
