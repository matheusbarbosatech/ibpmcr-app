@echo off
chcp 65001 > nul
title IBPM CR Super-App - Teste no Navegador Web
cd /d "c:\Users\matheus\Desktop\ibpmcr-app"
echo =================================================================
echo 🌐 ABRINDO O SUPER-APP OFICIAL IBPM CR NO NAVEGADOR (CHROME/EDGE)...
echo =================================================================
echo.
python run_local.py web
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ocorreu um erro ao rodar o aplicativo no navegador.
    pause
)
