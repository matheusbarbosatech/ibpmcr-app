@echo off
title IBPM CR - Auto Deploy Celular + Scrcpy
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo AUTO-DEPLOY: ENVIAR APK, INSTALAR NO CELULAR E ABRIR SCRCPY...
echo =================================================================
"%PYTHON_EXE%" scripts\auto_deploy_android.py
pause
