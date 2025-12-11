import os
import sys
import configparser
import subprocess
import re
from pathlib import Path

# --- CONFIGURATION ---
# Note: yt-dlp.exe and ffmpeg.exe must be in the same folder as this script.
# The batch file ensures this.
YTDLP_EXE = Path(os.path.dirname(os.path.abspath(__file__))) / 'yt-dlp.exe'
FFMPEG_EXE = Path(os.path.dirname(os.path.abspath(__file__))) / 'ffmpeg.exe'
# ---------------------

def get_song_metadata(folder_path):
    """Reads the song.ini or notes.chart file to get Artist and Name."""
    ini_path = os.path.join(folder_path, "song.ini")
    chart_path = os.path.join(folder_path, "notes.chart")
    
    # 1. Try to read song.ini first
    if os.path.exists(ini_path):
        try:
            config = configparser.ConfigParser(strict=False)
            config.read(ini_path)
            if 'song' in config:
                name = config['song'].get('name', '').strip()
                artist = config['song'].get('artist', '').strip()
                if name and artist:
                    return artist, name
        except Exception:
            pass

    # 2. Fallback to notes.chart
    if os.path.exists(chart_path):
        try:
            with open(chart_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            artist_match = re.search(r'Artist\s*=\s*"([^"]+)"', content, re.IGNORECASE)
            name_match = re.search(r'Name\s*=\s*"([^"]+)"', content, re.IGNORECASE)
            
            artist = artist_match.group(1).strip() if artist_match else ''
            name = name_match.group(1).strip() if name_match else ''

            if name and artist:
                return artist, name

        except Exception:
            pass
            
    return None, None

def download_and_convert_video(folder_path, artist, song_name):
    """Uses yt-dlp to search, download, and convert the video."""
    
    # Check if video already exists (Clone Hero looks for video.webm)
    if os.path.exists(os.path.join(folder_path, "video.webm")):
        return False # Video already exists, nothing to do
        
    print(f" -> Searching & Downloading video for: {artist} - {song_name}")
    
    # Construct the search query
    query = f"ytsearch1:{artist} - {song_name} official video"
    output_path = os.path.join(folder_path, "video.webm")
    
    # ** COMPATIBILITY OPTIMIZATION **
    # Using 'good' quality and fixed 2M bitrate for maximum Clone Hero compatibility.
    quality_flags = "-quality good -speed 0 -threads 0"
    conversion_args = f"-c:v libvpx -b:v 2M -c:a libvorbis {quality_flags}"
    
    command = [
        str(YTDLP_EXE),
        query,
        "-f", "bestvideo+bestaudio/best",
        "--recode-video", "webm",
        "--postprocessor-args", conversion_args,
        "-o", output_path,
        "--no-playlist",
        "--quiet",
        "--no-warnings"
    ]
    
    try:
        subprocess.run(command, check=True)
        print(" -> Download and Conversion Complete (STABLE).")
        return True
    except subprocess.CalledProcessError as e:
        print(f" -> ERROR: Download/Conversion failed. (Code: {e.returncode})")
        return False
    except FileNotFoundError:
        print(" -> ERROR: yt-dlp.exe or ffmpeg.exe not found in utility folder!")
        sys.exit(1)


def process_songs_folder(songs_path):
    """Iterates through all song folders to download missing videos."""
    downloaded_count = 0
    print("--- Starting Automatic Video Search and Download ---")
    
    # Use os.walk to recursively find all subfolders
    for root, dirs, files in os.walk(songs_path):
        # Check if the current directory is a song folder (i.e., contains song.ini or notes.chart)
        if 'song.ini' in files or 'notes.chart' in files:
            artist, name = get_song_metadata(root)
            
            if artist and name and not artist == 'Unknown':
                if download_and_convert_video(root, artist, name):
                    downloaded_count += 1
            else:
                print(f"Skipping folder '{Path(root).name}': Could not find Artist/Name metadata.")

    print(f"\n--- Download Summary ---")
    print(f"Total new videos downloaded and converted: {downloaded_count}")
    return downloaded_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python auto_downloader.py <path_to_songs_folder>")
        sys.exit(1)
        
    songs_folder_path = sys.argv[1]
    
    if not os.path.isdir(songs_folder_path):
        print(f"Error: Folder not found at {songs_folder_path}")
        sys.exit(1)
        
    process_songs_folder(songs_folder_path)