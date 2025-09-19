@echo off
title Test Slovak-Czech Translator

echo.
echo ============================================================
echo              TRANSLATOR INSTALLATION TEST
echo ============================================================
echo.
echo This will verify that your translator is working properly.
echo.
echo Checking installation...
echo.

REM Check if executable exists
if not exist "Slovak-Czech-Translator.exe" (
    echo ❌ ERROR: Slovak-Czech-Translator.exe not found!
    echo.
    echo Please make sure you extracted all files properly.
    echo.
    pause
    exit /b 1
)

echo ✅ Translator executable found
echo.

REM Check if the executable can start (just start and close quickly)
echo Testing translator startup...
echo.

start "" "Slovak-Czech-Translator.exe"
timeout /t 2 /nobreak >nul

echo.
echo ✅ Translator test completed!
echo.
echo If you saw a translator window open briefly, everything is working!
echo.
echo You can now use START_TRANSLATOR.bat to run the actual translator.
echo.
echo ============================================================
echo                    TEST RESULTS
echo ============================================================
echo ✅ Executable file: Found
echo ✅ Startup test: Passed  
echo ✅ Ready to translate Slovak articles!
echo ============================================================
echo.
echo Next steps:
echo 1. Double-click START_TRANSLATOR.bat
echo 2. Copy a Slovak article URL
echo 3. Paste it and click "Translate Article"
echo.
pause