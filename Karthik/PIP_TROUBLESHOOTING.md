# Pip Troubleshooting Guide for Windows

## Issue: "pip is not recognized" or "No module named pip"

### Solution 1: Install pip using ensurepip (Recommended)
```powershell
python -m ensurepip --upgrade
```

### Solution 2: Use python -m pip instead of pip
Instead of:
```powershell
pip install package
```

Use:
```powershell
python -m pip install package
```

### Solution 3: Download and install pip manually
1. Download `get-pip.py` from https://bootstrap.pypa.io/get-pip.py
2. Run: `python get-pip.py`

## Common Commands

### Check pip version
```powershell
python -m pip --version
```

### Install packages
```powershell
python -m pip install package_name
python -m pip install -r requirements.txt
```

### Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### List installed packages
```powershell
python -m pip list
```

### Uninstall package
```powershell
python -m pip uninstall package_name
```

## For This Project

All dependencies are now installed. You can proceed with:

1. **Set up database:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create admin user:**
   ```powershell
   python setup.py
   ```

3. **Run server:**
   ```powershell
   python manage.py runserver
   ```

## Notes

- On Windows, always use `python -m pip` instead of just `pip` to avoid path issues
- If you have multiple Python versions, specify the version: `python3.13 -m pip`
- Make sure Python is added to your PATH environment variable

