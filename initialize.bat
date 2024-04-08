@echo off

REM Task 1: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    exit /b
)

echo Python is installed.

REM Task 2: Check if pip is updated
python -m pip install --upgrade pip > nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to update pip.
    exit /b
)

echo Pip is updated.

REM Task 3: Check if treelib is installed
pip show treelib > nul 2>&1
if %errorlevel% neq 0 (
    echo Treelib is not installed. Installing...
    pip install treelib > nul 2>&1
    if %errorlevel% neq 0 (
        echo Failed to install treelib.
        exit /b
    )
    echo Treelib is now installed.
) else (
    echo Treelib is already installed.
)

REM Task 4: Check if PySide6 is installed
pip show PySide6 > nul 2>&1
if %errorlevel% neq 0 (
    echo PySide6 is not installed. Installing...
    pip install PySide6 > nul 2>&1
    if %errorlevel% neq 0 (
        echo Failed to install PySide6.
        exit /b
    )
    echo PySide6 is now installed.
) else (
    echo PySide6 is already installed.
)

REM Task 5: Run game.py
echo Running game.py...
python game.py
