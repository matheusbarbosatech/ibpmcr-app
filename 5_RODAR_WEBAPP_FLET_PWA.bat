@echo off
title IBPM CR - WebApp PWA Oficial em Python Flet
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo 🔥 INICIANDO SUPER-APP OFICIAL IBPM CR NO NAVEGADOR (FLET PWA)...
echo =================================================================
echo 📱 Porta: http://localhost:8550
echo 💡 PWA com Suporte a Instalacao e Funcionamento Offline
echo =================================================================
"%PYTHON_EXE%" run_local.py web
echo =================================================================
echo Servidor Flet Web encerrado.
echo =================================================================
pause
