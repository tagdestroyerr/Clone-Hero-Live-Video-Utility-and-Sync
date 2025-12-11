@echo off
setlocal enableDelayedExpansion

:: Set the script's directory path (ends with a backslash)
set "SCRIPT_DIR=%~dp0"

:: --- Config & Dependency Checks ---
set "FFMPEG_EXE=!SCRIPT_DIR!ffmpeg.exe"
set "YTDLP_EXE=!SCRIPT_DIR!yt-dlp.exe"
set "SYNC_INI_SCRIPT=!SCRIPT_DIR!sync_ini.py"
set "AUTO_DOWNLOADER_SCRIPT=!SCRIPT_DIR!auto_downloader.py"
set "VIDEO_PROCESSOR_SCRIPT=!SCRIPT_DIR!video_processor.py"
set "PYTHON_EXE=python.exe"

if not exist "!SCRIPT_DIR!ffmpeg.exe" (
    echo.
    echo ERROR: Required file missing: ffmpeg.exe
    echo Please ensure ffmpeg.exe is in the same folder as this script.
    pause
    exit /b 1
)
if not exist "!SCRIPT_DIR!yt-dlp.exe" (
    echo.
    echo ERROR: Required file missing: yt-dlp.exe
    echo Please ensure yt-dlp.exe is in the same folder as this script.
    pause
    exit /b 1
)
if not exist "!SYNC_INI_SCRIPT!" (
    echo.
    echo ERROR: Required file missing: sync_ini.py
    echo Please ensure sync_ini.py is in the same folder as this script.
    pause
    exit /b 1
)
if not exist "!VIDEO_PROCESSOR_SCRIPT!" (
    echo.
    echo ERROR: Required file missing: video_processor.py
    echo Please ensure video_processor.py is in the same folder as this script.
    pause
    exit /b 1
)

:: ** CRITICAL FIX: Check Python availability before configuration reading **
set "PYTHON_AVAILABLE=false"
"%PYTHON_EXE%" -V >NUL 2>&1
if not ERRORLEVEL 1 (
    set "PYTHON_AVAILABLE=true"
)
:: ------------------------------------------------------------------------

:: --- Set Menu Text Safely ---
if exist "!AUTO_DOWNLOADER_SCRIPT!" (
    set "OPTION_2_TEXT=2. AUTOMATIC DOWNLOAD ^& SYNC (Search, Download, Convert, AND Fix INI Files)"
) else (
    set "OPTION_2_TEXT=2. AUTOMATIC DOWNLOAD ^& SYNC (DISABLED - auto_downloader.py missing)"
)

:: --- 1. Get Songs Folder via Drag-and-Drop ---
if "%~1"=="" (
    echo.
    echo CLONE HERO VIDEO UTILITY
    echo =========================
    echo Please drag your main "Clone Hero\Songs" folder onto this script
    echo and press Enter to begin the process.
    pause
    exit /b 1
)

set "SONGS_DIR=%~1"

:MENU
cls

:: Read and display current settings
set "CURRENT_RES_W=1280"
set "CURRENT_BITRATE=2M"

if "!PYTHON_AVAILABLE!"=="true" (
    :: Only attempt to read config if Python is available
    for /f "delims=" %%i in ('"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" --get-config max_width 2^>NUL') do (
        set "CURRENT_RES_W=%%i"
    )
    for /f "delims=" %%i in ('"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" --get-config max_bitrate 2^>NUL') do (
        set "CURRENT_BITRATE=%%i"
    )
) else (
    echo WARNING: Python not found. Using default resolution and bitrate.
)

echo.
echo =======================================================
echo CLONE HERO VIDEO UTILITY MENU
echo Songs Folder Set To: "!SONGS_DIR!"
echo -------------------------------------------------------
echo Current Video Resolution: Max Width !CURRENT_RES_W! (e.g. 1920=1080p, 1280=720p)
echo Current Video Bitrate: !CURRENT_BITRATE!
echo =======================================================
echo 1. MANUAL DOWNLOAD (URL input, Creates WEBM)
echo !OPTION_2_TEXT!
echo 3. FIX/CONVERT Existing MP4s to WEBM (Fallback)
echo 4. SYNC INI FILES ONLY (Fix timing AND loading error)
echo 6. Change Video Settings
echo 5. Exit
echo.
set /p CHOICE="Select an option (1, 2, 3, 4, 5, or 6): "

if /i "%CHOICE%"=="1" goto MANUAL_DOWNLOAD
if /i "%CHOICE%"=="2" goto AUTO_DOWNLOAD_AND_SYNC
if /i "%CHOICE%"=="3" goto CONVERT
if /i "%CHOICE%"=="4" goto SYNC_INI
if /i "%CHOICE%"=="5" goto END
if /i "%CHOICE%"=="6" goto SET_VIDEO_CONFIG
goto MENU

:: --- 2. Manual Downloader Routine (New Python Wrapper Call) ---
:MANUAL_DOWNLOAD
cls
if "!PYTHON_AVAILABLE!"=="false" (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH. Cannot run Option 1.
    pause
    goto MENU
)

echo.
echo =======================================================
echo MANUAL VIDEO DOWNLOADER (URL Required)
echo =======================================================

echo.
echo Using Resolution Width: !CURRENT_RES_W! | Bitrate: !CURRENT_BITRATE!
echo.
set /p VIDEO_URL="Enter the YouTube URL: "
set /p SONG_FOLDER="Enter the FULL path to the Song Folder: "

echo.
echo Downloading and Encoding video from: %VIDEO_URL%

:: Call the new Python wrapper for download
:: ** FIX: Ensure the Python script path is correctly quoted and executed via CALL **
set "PYTHON_CMD=^"%PYTHON_EXE%^" ^"!VIDEO_PROCESSOR_SCRIPT%!^" download ^"%VIDEO_URL%^" ^"%SONG_FOLDER%\video.webm^" ^"!CURRENT_RES_W%!^" ^"!CURRENT_BITRATE%!^""
CALL !PYTHON_CMD!

echo.
echo DOWNLOAD ^& ENCODING COMPLETE.
pause
goto MENU


:: --- 3. Combined Automatic Download and Sync Routine ---
:AUTO_DOWNLOAD_AND_SYNC
if not exist "!AUTO_DOWNLOADER_SCRIPT!" (
    echo.
    echo ERROR: auto_downloader.py script not found. Cannot run Option 2.
    pause
    goto MENU
)
cls
if "!PYTHON_AVAILABLE!"=="false" (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH. Cannot run Option 2.
    pause
    goto MENU
)

echo.
echo =======================================================
echo AUTOMATIC VIDEO DOWNLOAD ^& INI SYNC
echo =======================================================
echo Python found. Running automatic download script...
echo.

:: STEP 1: Execute the Auto Downloader Python script
"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" "!SONGS_DIR!"

echo.
echo -------------------------------------------------------
echo Running INI Synchronization...
echo -------------------------------------------------------

:: STEP 2: Execute the INI Sync Python script
"%PYTHON_EXE%" "!SYNC_INI_SCRIPT!" "!SONGS_DIR!"

echo.
echo =======================================================
echo AUTOMATIC DOWNLOAD ^& SYNC COMPLETE.
echo =======================================================
pause
goto MENU


:: --- 4. Fallback Conversion Routine (New Python Wrapper Call) ---
:CONVERT
cls
if "!PYTHON_AVAILABLE!"=="false" (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH. Cannot run Option 3.
    pause
    goto MENU
)

echo.
echo =======================================================
echo FALLBACK CONVERSION (MP4 to WEBM)
echo =======================================================

echo.
echo Using Resolution Width: !CURRENT_RES_W! | Bitrate: !CURRENT_BITRATE!
echo This is for existing MP4 files that need conversion.
echo Target Directory: "!SONGS_DIR!"
echo.

set /a CONVERTED_COUNT=0

for /R "%SONGS_DIR%" %%f in (*.mp4) do (
    echo.
    echo Converting: "%%f"
    
    :: Call the new Python wrapper for conversion
    :: ** FIX: Ensure the Python script path is correctly quoted and executed via CALL **
    set "PYTHON_CMD=^"%PYTHON_EXE%^" ^"!VIDEO_PROCESSOR_SCRIPT%!^" convert ^"%%f^" ^"%%~dpnf.webm^" ^"!CURRENT_RES_W%!^" ^"!CURRENT_BITRATE%!^""
    CALL !PYTHON_CMD!
    
    if exist "%%~dpnf.webm" (
        echo Success. Output: "%%~dpnf.webm"
        set /a CONVERTED_COUNT+=1
    ) else (
        echo ERROR: Python wrapper reported a failure or file was not created.
    )
)

echo.
echo =======================================================
echo FALLBACK CONVERSION COMPLETE! Processed !CONVERTED_COUNT! files.
echo =======================================================
pause
goto MENU

:: --- 5. INI Sync and Repair Routine ---
:SYNC_INI
cls
if "!PYTHON_AVAILABLE!"=="false" (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH. Cannot run Option 4.
    pause
    goto MENU
)

echo.
echo =======================================================
echo INI SYNCHRONIZATION
echo =======================================================
echo Python found. Running sync and repair script on: "!SONGS_DIR!"
echo.

:: Execute the Python script, passing the songs directory as an argument
"%PYTHON_EXE%" "!SYNC_INI_SCRIPT!" "!SONGS_DIR!"

echo.
echo =======================================================
echo INI SYNCHRONIZATION COMPLETE.
echo =======================================================
pause
goto MENU

:: --- 6. Set Video Config Routine ---
:SET_VIDEO_CONFIG
cls
if "!PYTHON_AVAILABLE!"=="false" (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH. Cannot run Option 6.
    pause
    goto MENU
)

echo.
echo =======================================================
echo VIDEO ENCODING SETTINGS
echo =======================================================

:: Read config values (using the currently set variables)
set "CURRENT_W=!CURRENT_RES_W!"
set "CURRENT_BR=!CURRENT_BITRATE!"

echo Current Max Resolution Width (1080p=1920, 720p=1280, 480p=854): !CURRENT_W!
set /p NEW_W="Enter NEW Max Resolution Width (e.g., 1920): "

echo.
echo Current Max Bitrate (High Quality=2M, Standard=1M, Low=500k): !CURRENT_BR!
set /p NEW_BR="Enter NEW Max Bitrate (e.g., 2M): "

echo.
echo Applying settings...

:: Set Max Width
"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" --set-config max_width "!NEW_W!"
if errorlevel 1 (
    echo ERROR: Failed to set Max Resolution. See console output for details.
    pause
    goto MENU
)

:: Set Max Bitrate
"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" --set-config max_bitrate "!NEW_BR!"
if errorlevel 1 (
    echo ERROR: Failed to set Max Bitrate. See console output for details.
    pause
    goto MENU
)

echo.
echo ALL VIDEO SETTINGS UPDATED SUCCESSFULLY!
pause
goto MENU

:END
echo.
echo Utility closed.
endlocal
exit