@echo off
title IBPM CR - Robo Agente de Testes Automaticos
set PYTHON_EXE=C:\Users\matheus\AppData\Local\Programs\Python\Python311\python.exe
set PATH=C:\Users\matheus\AppData\Local\Programs\Python\Python311;C:\Users\matheus\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
cd /d C:\Users\matheus\Desktop\ibpmcr-app
echo =================================================================
echo 🤖 INICIANDO AGENTE AUTONOMO DE TESTES - IBPM CARVALHO RAMOS
echo =================================================================
echo 🎯 Testando 100%% das Telas, Botoes, Modais, Audios e Banco SQLite
echo =================================================================
"%PYTHON_EXE%" robo_testes_ibpmcr.py
echo =================================================================
echo Auditoria do Robo concluida.
echo =================================================================
pause
