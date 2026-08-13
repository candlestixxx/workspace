@echo off
cd /d "C:\Users\jakeg\workspace\Prank-Deck-AI"
if not exist "package.json" (
    echo ERROR: package.json not found!
    echo Expected at: C:\Users\jakeg\workspace\Prank-Deck-AI\package.json
    dir "C:\Users\jakeg\workspace\Prank-Deck-AI"
    pause
    exit /b 1
)
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
echo.
echo ==============================
echo  PrankDeck Studio
echo  http://localhost:5173
echo ==============================
echo.
call npm run dev
pause
