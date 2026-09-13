@echo off
title IBPM CR - Diagnostico e Testes
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo EXECUTANDO BATERIA DE TESTES AUTOMATIZADOS...
echo =================================================================
"%PYTHON_EXE%" test_app.py
echo =================================================================
pause
