@echo off
setlocal enableDelayedExpansion

:: Set the script's directory path (ends with a backslash)
set "SCRIPT_DIR=%~dp0"

:: --- Config & Dependency Checks ---
set "FFMPEG_EXE=!SCRIPT_DIR!ffmpeg.exe"
set "YTDLP_EXE=!SCRIPT_DIR!yt-dlp.exe"
set "SYNC_INI_SCRIPT=!SCRIPT_DIR!sync_ini.py"
set "AUTO_DOWNLOADER_SCRIPT=!SCRIPT_DIR!auto_downloader.py"
set "PYTHON_EXE=python.exe"

if not exist "!FFMPEG_EXE!" (
    echo.
    echo ERROR: Required file missing: ffmpeg.exe
    echo Please ensure ffmpeg.exe is in the same folder as this script.
    pause
    exit /b 1
)

if not exist "!YTDLP_EXE!" (
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

:: --- Set Menu Text Safely (Fixes previous display errors) ---
if exist "!AUTO_DOWNLOADER_SCRIPT!" (
    set "OPTION_2_TEXT=2. AUTOMATIC DOWNLOAD & SYNC (Search, Download, Convert, AND Fix INI Files)"
) else (
    set "OPTION_2_TEXT=2. AUTOMATIC DOWNLOAD & SYNC (DISABLED - auto_downloader.py missing)"
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
echo.
echo =======================================================
echo CLONE HERO VIDEO UTILITY MENU
echo Songs Folder Set To: "!SONGS_DIR!"
echo =======================================================
echo 1. MANUAL DOWNLOAD (URL input, Creates WEBM)
echo !OPTION_2_TEXT!
echo 3. FIX/CONVERT Existing MP4s to WEBM (Fallback)
echo 4. SYNC INI FILES ONLY (Fix timing AND loading error)
echo 5. Exit
echo.
set /p CHOICE="Select an option (1, 2, 3, 4, or 5): "

if /i "%CHOICE%"=="1" goto MANUAL_DOWNLOAD
if /i "%CHOICE%"=="2" goto AUTO_DOWNLOAD_AND_SYNC
if /i "%CHOICE%"=="3" goto CONVERT
if /i "%CHOICE%"=="4" goto SYNC_INI
if /i "%CHOICE%"=="5" goto END
goto MENU

:: --- 2. Manual Downloader Routine ---
:MANUAL_DOWNLOAD
cls
echo.
echo =======================================================
echo MANUAL VIDEO DOWNLOADER (URL Required)
echo =======================================================
echo.
echo INSTRUCTIONS:
echo 1. Get the URL for the song video.
echo 2. Get the full path to the specific Clone Hero song folder.
echo 3. The final video will be saved as "video.webm" in that folder.
echo.
set /p VIDEO_URL="Enter the YouTube URL: "
set /p SONG_FOLDER="Enter the FULL path to the Song Folder: "

echo.
echo Downloading and Encoding video from: %VIDEO_URL%
echo Saving to: %SONG_FOLDER%\video.webm

:: ** COMPATIBILITY OPTIMIZATION **
CALL "!YTDLP_EXE!" -f "bestvideo+bestaudio/best" --recode-video webm --postprocessor-args "-c:v libvpx -b:v 2M -c:a libvorbis -quality good -speed 0 -threads 0" -o "%SONG_FOLDER%\video.webm" "%VIDEO_URL%"

echo.
echo DOWNLOAD & ENCODING COMPLETE.
echo REMINDER: You should run Option 4 (SYNC INI FILES ONLY) if the song does not load or sync correctly.
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
echo.
echo =======================================================
echo AUTOMATIC VIDEO DOWNLOAD AND INI SYNC
echo (Scanning: "!SONGS_DIR!")
echo =======================================================
echo Checking for Python...
"%PYTHON_EXE%" -V >NUL 2>&1
if ERRORLEVEL 1 (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH.
    echo You must install Python to use this feature.
    pause
    goto MENU
)

echo Python found. Running automatic download script...
echo.

:: STEP 1: Execute the Auto Downloader Python script
"%PYTHON_EXE%" "!AUTO_DOWNLOADER_SCRIPT!" "!SONGS_DIR!"

echo.
echo -------------------------------------------------------
echo Running INI Synchronization for all downloaded videos...
echo -------------------------------------------------------

:: STEP 2: Execute the INI Sync Python script
"%PYTHON_EXE%" "!SYNC_INI_SCRIPT!" "!SONGS_DIR!"

echo.
echo =======================================================
echo AUTOMATIC DOWNLOAD & SYNC COMPLETE.
echo =======================================================
pause
goto MENU


:: --- 4. Fallback Conversion Routine ---
:CONVERT
cls
echo.
echo =======================================================
echo FALLBACK CONVERSION (MP4 to VP8 WEBM)
echo =======================================================
echo This is for existing MP4 files that need conversion.
echo Target Directory: "!SONGS_DIR!"
echo.

set /a CONVERTED_COUNT=0

for /R "%SONGS_DIR%" %%f in (*.mp4) do (
    echo.
    echo ---
    echo Converting: "%%f"
    
    set "INPUT_FILE=%%f"
    set "OUTPUT_FILE=%%~dpnf.webm"
    
    :: ** COMPATIBILITY OPTIMIZATION **
    CALL "!FFMPEG_EXE!" -i "!INPUT_FILE!" -c:v libvpx -b:v 2M -c:a libvorbis -quality good -speed 0 -threads 0 -y "!OUTPUT_FILE!"
    
    if exist "!OUTPUT_FILE!" (
        echo Success. Output: "!OUTPUT_FILE!"
        set /a CONVERTED_COUNT+=1
    ) else (
        echo ERROR: FFmpeg failed to create the WEBM file.
    )
    echo ---
)

echo.
echo =======================================================
echo FALLBACK CONVERSION COMPLETE! Processed !CONVERTED_COUNT! files.
echo REMINDER: Run Option 4 (SYNC INI FILES ONLY) next!
echo =======================================================
pause
goto MENU

:: --- 5. INI Sync and Repair Routine (Uses Updated Python) ---
:SYNC_INI
cls
echo.
echo =======================================================
echo INI SYNCHRONIZATION AND REPAIR (Fixing loading AND timing)
echo =======================================================
echo Checking for Python...
"%PYTHON_EXE%" -V >NUL 2>&1
if ERRORLEVEL 1 (
    echo.
    echo ERROR: Python is NOT installed or not in the system PATH.
    echo You must install Python to use this feature.
    pause
    goto MENU
)
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


:END
echo.
echo Utility closed.
endlocal
exit