import os

bat1 = """@echo off
title IBPM CR - Teste Local Desktop
set PYTHON_EXE=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\python.exe
set PATH=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
cd /d C:\\Users\\matheus\\Desktop\\ibpmcr-app
echo =================================================================
echo ABRINDO SUPER-APP OFICIAL IBPM CR NO SEU COMPUTADOR...
echo =================================================================
"%PYTHON_EXE%" run_local.py desktop
echo =================================================================
echo Aplicativo finalizado.
echo =================================================================
pause
"""

bat2 = """@echo off
title IBPM CR - Teste no Navegador Web
set PYTHON_EXE=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\python.exe
set PATH=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
cd /d C:\\Users\\matheus\\Desktop\\ibpmcr-app
echo =================================================================
echo ABRINDO SUPER-APP OFICIAL IBPM CR NO NAVEGADOR (CHROME/EDGE)...
echo =================================================================
"%PYTHON_EXE%" run_local.py web
echo =================================================================
echo Servidor Web encerrado.
echo =================================================================
pause
"""

bat3 = """@echo off
title IBPM CR - Hot Reload (Atualizacao em Tempo Real)
set PYTHON_EXE=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\python.exe
set PATH=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
cd /d C:\\Users\\matheus\\Desktop\\ibpmcr-app
echo =================================================================
echo INICIANDO COM HOT-RELOAD (ATUALIZACAO EM TEMPO REAL)
echo =================================================================
"C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\flet.exe" run main.py -r
echo =================================================================
echo Flet Hot Reload finalizado.
echo =================================================================
pause
"""

bat4 = """@echo off
title IBPM CR - Diagnostico e Testes
set PYTHON_EXE=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\python.exe
set PATH=C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\matheus\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
cd /d C:\\Users\\matheus\\Desktop\\ibpmcr-app
echo =================================================================
echo EXECUTANDO BATERIA DE TESTES AUTOMATIZADOS...
echo =================================================================
"%PYTHON_EXE%" test_app.py
echo =================================================================
pause
"""

files = {
    r"c:\Users\matheus\Desktop\ibpmcr-app\1_RODAR_APP_NO_PC.bat": bat1,
    r"C:\Users\matheus\Desktop\1_RODAR_APP_NO_PC.bat": bat1,
    r"c:\Users\matheus\Desktop\ibpmcr-app\2_RODAR_APP_NAVEGADOR.bat": bat2,
    r"C:\Users\matheus\Desktop\2_RODAR_APP_NAVEGADOR.bat": bat2,
    r"c:\Users\matheus\Desktop\ibpmcr-app\3_RODAR_COM_HOT_RELOAD.bat": bat3,
    r"C:\Users\matheus\Desktop\3_RODAR_COM_HOT_RELOAD.bat": bat3,
    r"c:\Users\matheus\Desktop\ibpmcr-app\4_TESTAR_SISTEMA_COMPLETO.bat": bat4,
    r"C:\Users\matheus\Desktop\4_TESTAR_SISTEMA_COMPLETO.bat": bat4,
}

for path, content in files.items():
    with open(path, "wb") as f:
        f.write(content.replace("\n", "\r\n").encode("ascii"))
    print("Escrito com sucesso:", path)

print("TODOS OS BATs GERADOS EM ASCII PURO COM SUCESSO!")
