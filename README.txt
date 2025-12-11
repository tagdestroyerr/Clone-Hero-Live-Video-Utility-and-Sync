=====================================================
CLONE HERO VIDEO UTILITY KIT v 2.0 (FINAL STABLE)
(DOWNLOADER, CONVERTER & AUTOMATIC INI SYNC)
=====================================================

### ⚠️ DISCLAIMER ⚠️

This tool is provided as-is for personal use. By using this kit, you acknowledge that you are using it at your own risk. 
The author takes no responsibility for any issues, errors, data loss, or other problems that may arise from its use. 
Always back up your files before running any new script.

---

### REQUIRED FILES

Ensure the following five files are in the same folder as this README:

1.  **CH_Video_Utility.bat** (The main script you run)
2.  **ffmpeg.exe** (The video conversion tool)
3.  **yt-dlp.exe** (The video download tool)
4.  **sync_ini.py** (The Python script for synchronization)
5.  **auto_downloader.py** (The Python script for automatic download)

### ⚠️ IMPORTANT: PYTHON REQUIREMENT ⚠️

To use **ANY** of the Python-based options (2 or 4), you **MUST** have **Python 3.x** installed on your system. 

Python can be downloaded from the official website. When installing, ensure the **"Add python.exe to PATH"** option is checked.

---

### STEP 1: PREPARATION

1.  Locate your main Clone Hero **"Songs" folder**. 
    (The default location is usually: C:\Users\YourName\Documents\Clone Hero\Songs)

### STEP 2: RUNNING THE UTILITY (Drag-and-Drop)

1.  Drag the icon of your main **"Songs" folder** onto the **"CH_Video_Utility.bat"** file.
2.  The utility will launch, set your Songs directory, and open the main menu.

---

### STEP 3: USE THE MENU (FINAL OPTIONS)

The utility is now optimized for **maximum compatibility** and **stable performance**.

#### 1. MANUAL DOWNLOAD (URL input, Creates WEBM)
* Select option **1** to download a single video from a specific URL.
* It uses the **stable compatibility encoding** to ensure the resulting `video.webm` file works perfectly in Clone Hero.

#### 2. AUTOMATIC DOWNLOAD & SYNC (RECOMMENDED)
* Select option **2** to automate the entire process for your entire library.
* **Action 1: Download & Convert (STABLE)**: Recursively scans all song folders, finds songs missing `video.webm`, 
searches YouTube, downloads the best match, and converts it to a compatible `.webm` file using the robust encoding settings.
* **Action 2: Sync INI**: Automatically runs the INI synchronization on all folders, ensuring the `video_start_time` 
setting is correct and the `video = video.webm` line is present.

#### 3. FIX/CONVERT Existing MP4s to WEBM (Fallback)
* Select option **3** to scan all song folders and convert any *existing* `.mp4` or other incompatible video files to the compatible **`.webm`** 
format using the stable conversion settings.

#### 4. SYNC INI FILES ONLY
* Select option **4** if you have manually added videos or charts and only need to correct the metadata. 
This runs the synchronization script to fix the video timing and loading errors without touching any video files.

---

### 💡 PERFORMANCE & TROUBLESHOOTING

#### Why Option 2 (Automatic Download) Appears to Pause

When the script displays a line like:
`-> Searching & Downloading video for: Artist - Song Name`

...the program is performing four essential, sequential steps for that single song: **Search, Download, Re-encode (Convert), and Save.**

The **Re-encode (Convert)** step is CPU-intensive and necessary for compatibility. 
The script only prints the "Download and Conversion Complete (STABLE)." line **AFTER all four steps are finished.** 
For longer videos, please be patient and allow the script time to complete the conversion.

#### If videos display a Black Screen or Do Not Load

1.  **Re-run Option 2:** The current **STABLE** encoding profile fixes files that the previous, faster profile may have broken. 
Delete the `video.webm` file for the problematic song(s) and run Option 2 again to force a stable re-conversion.
2.  In Clone Hero, go to **Settings** → **Gameplay** and ensure **Backgrounds** is set to **Video** or **On**.
3.  In Clone Hero, go to **Settings** → **Video** and ensure no visual effects (like "Highway Background") are blocking the video layer.
4.  Ensure you have re-scanned your songs in Clone Hero after running the utility (**Settings** → **General** → **Scan Songs**).