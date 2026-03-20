@echo off
title Mathnasium PAR Comment Tool - Setup
echo ================================
echo  Mathnasium PAR Comment Tool
echo ================================
echo.

:: Check if Python is installed
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Opening download page...
    echo Please install Python from python.org
    echo IMPORTANT: Check "Add python.exe to PATH" during install!
    start https://www.python.org/downloads/
    echo.
    echo After installing Python, double-click this file again.
    pause
    exit
)
echo Python found!

:: Check and install pip packages
echo.
echo Checking Playwright...
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Playwright... this may take a minute.
    python -m pip install playwright
)
echo Playwright found!

:: Check if Chromium is installed
echo.
echo Checking Chromium browser...
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.stop()" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Chromium... this may take a few minutes.
    python -m playwright install chromium
)
echo Chromium found!

:: All good — launch the app
echo.
echo ================================
echo  All good! Launching app...
echo ================================
echo.
python app.py
