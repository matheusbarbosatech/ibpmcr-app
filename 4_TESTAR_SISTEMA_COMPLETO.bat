@echo off
chcp 65001 > nul
title IBPM CR Super-App - Diagnostico e Testes
cd /d "c:\Users\matheus\Desktop\ibpmcr-app"
echo =================================================================
echo 🧪 EXECUTANDO DIAGNÓSTICO E BATERIA DE TESTES AUTOMATIZADOS...
echo =================================================================
echo.
python test_app.py
echo.
pause
