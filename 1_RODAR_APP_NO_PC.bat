@echo off
title IBPM CR - Teste Local Desktop
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo ABRINDO SUPER-APP OFICIAL IBPM CR NO SEU COMPUTADOR...
echo =================================================================
"%PYTHON_EXE%" run_local.py desktop
echo =================================================================
echo Aplicativo finalizado.
echo =================================================================
pause
