@echo off
chcp 65001 > nul
title IBPM CR Super-App - Hot Reload (Atualizacao em Tempo Real)
cd /d "c:\Users\matheus\Desktop\ibpmcr-app"
echo =================================================================
echo 🔥 INICIANDO COM HOT-RELOAD (ATUALIZAÇÃO EM TEMPO REAL)
echo =================================================================
echo Toda alteração no código atualiza a tela automaticamente!
echo.
flet run main.py -r
if %errorlevel% neq 0 (
    echo.
    echo ❌ Flet runner encerrou.
    pause
)
