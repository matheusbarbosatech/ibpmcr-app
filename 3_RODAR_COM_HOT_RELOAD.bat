@echo off
title IBPM CR - Hot Reload (Atualizacao em Tempo Real)
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo INICIANDO COM HOT-RELOAD (ATUALIZACAO EM TEMPO REAL)
echo =================================================================
"C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts\flet.exe" run main.py -r
echo =================================================================
echo Flet Hot Reload finalizado.
echo =================================================================
pause
