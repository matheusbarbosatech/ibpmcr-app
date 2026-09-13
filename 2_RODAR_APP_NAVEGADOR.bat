@echo off
title IBPM CR - Teste no Navegador Web
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo ABRINDO SUPER-APP OFICIAL IBPM CR NO NAVEGADOR (CHROME/EDGE)...
echo =================================================================
"%PYTHON_EXE%" run_local.py web
echo =================================================================
echo Servidor Web encerrado.
echo =================================================================
pause
