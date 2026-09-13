@echo off
chcp 65001 > nul
title IBPM CR Super-App - Teste Local Desktop
cd /d "c:\Users\matheus\Desktop\ibpmcr-app"
echo =================================================================
echo 📱 ABRINDO O SUPER-APP OFICIAL IBPM CR NO SEU PC...
echo =================================================================
echo.
python run_local.py desktop
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ocorreu um erro ao rodar o aplicativo.
    pause
)
