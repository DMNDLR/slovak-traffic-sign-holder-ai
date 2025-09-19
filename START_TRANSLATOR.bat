@echo off
title Slovak-Czech Article Translator

echo.
echo ============================================================
echo         SLOVAK-CZECH ARTICLE TRANSLATOR v1.0
echo ============================================================
echo.
echo Starting translator application...
echo.
echo If Windows shows a security warning:
echo   - Click "More info" 
echo   - Then click "Run anyway"
echo.
echo The translator window should open in a few seconds...
echo.

REM Start the translator executable
start "" "Slovak-Czech-Translator.exe"

REM Check if it started successfully
timeout /t 3 /nobreak >nul

echo.
echo ✅ Translator started successfully!
echo.
echo You can now:
echo 1. Copy a Slovak article URL 
echo 2. Paste it into the translator window
echo 3. Click "Translate Article"
echo 4. Wait for completion
echo.
echo 💡 This window can be closed once the translator opens.
echo.
pause