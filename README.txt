Clone Hero Video Utility (CHVU)

This utility is designed to streamline the process of finding, downloading, converting, and synchronizing videos for your Clone Hero song library.

**STATUS: WORK IN PROGRESS (BETA)**

---

## ✅ Reliably Working Features (Core Functionality)

The primary automated functions are stable and functional.

| Option | Description | Status |
| :--- | :--- | :--- |
| **2** | **AUTOMATIC DOWNLOAD & SYNC** | **STABLE** |
| **6** | Change Video Settings | **STABLE** |

### 1. Primary Function (Option 2)

**Option 2** provides the core, reliable functionality:
* It searches for missing videos based on your song folder name.
* It downloads the best available video/audio streams.
* It converts the video to the required **WEBM format** (1280px wide default).
* It runs the Python script (`sync_ini.py`) to fix video timing, loading errors, and set the video path in the `song.ini` files.

**If you primarily rely on the automatic searching and processing, this option works perfectly.**

### 2. Changing Video Settings (Option 6)

**Option 6** allows you to configure the output video encoding quality:
* **Max Resolution Width:** (e.g., 1920 for 1080p, 1280 for 720p).
* **Max Bitrate:** (e.g., 2M for high quality, 1M for standard).

---

## ❌ Known Issues (Crashing)

The following functions currently fail due to persistent Command Prompt execution errors that are under active investigation:

| Option | Description | Status |
| :--- | :--- | :--- |
| **1** | MANUAL DOWNLOAD (URL input) | **CRASHING** |
| **3** | FIX/CONVERT Existing MP4s to WEBM (Fallback) | **CRASHING** |
| **4** | SYNC INI FILES ONLY | **CRASHING** |

**Please avoid using Options 1, 3, and 4 for now.** We will continue debugging these execution paths to ensure stability.

If you enjoy this or this was useful to you please consider supporting me by sending coffee money :) https://buymeacoffee.com/tagdestroyerr
