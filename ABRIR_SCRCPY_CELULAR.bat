@echo off
title IBPM CR - Espelhar Celular Scrcpy
set ADB_EXE=C:\Users\matheus\AppData\Local\Android\Sdk\platform-tools\adb.exe
set SCRCPY_EXE=C:\Users\matheus\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v4.1\scrcpy.exe
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo CONECTANDO AO CELULAR XIAOMI VIA ADB / SCRCPY...
echo =================================================================
"%ADB_EXE%" connect 192.168.1.8:5555
"%SCRCPY_EXE%" -s 192.168.1.8:5555 --window-title "IBPM CR - Celular Xiaomi" --stay-awake
pause
