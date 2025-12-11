import os
import sys
import configparser
import subprocess
import re
from pathlib import Path

# --- CONFIGURATION PATHS ---
YTDLP_EXE = Path(os.path.dirname(os.path.abspath(__file__))) / 'yt-dlp.exe'
FFMPEG_EXE = Path(os.path.dirname(os.path.abspath(__file__))) / 'ffmpeg.exe'
CONFIG_FILE = Path(os.path.dirname(os.path.abspath(__file__))) / 'video_config.ini'
DEFAULT_CONFIG = {
    'video': {
        'max_width': '1280', # 720p equivalent (width)
        'max_bitrate': '2M'  # High quality
    }
}

# --- CONFIG MANAGEMENT FUNCTIONS ---

def get_config():
    """Reads or creates the configuration file."""
    config = configparser.ConfigParser(interpolation=None, strict=False)
    
    # Try reading the existing file
    config.read(CONFIG_FILE)

    # If the file was not read successfully, or section is missing, set defaults
    if not config.sections() or 'video' not in config:
        config.read_dict(DEFAULT_CONFIG)
        # Only save if we created the defaults
        if not CONFIG_FILE.exists():
             try:
                print(f" -> Creating default config file at: {CONFIG_FILE.name}")
                save_config(config)
             except Exception:
                 pass
        
    # Ensure all default keys are present in the 'video' section
    elif 'video' in config:
        for key, value in DEFAULT_CONFIG['video'].items():
            if key not in config['video']:
                config['video'][key] = value
                save_config(config)
                
    return config

def save_config(config):
    """Writes the configuration file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    except IOError as e:
        print(f"ERROR: Could not write to config file: {e}")

# --- METADATA FUNCTIONS ---

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

# --- DOWNLOAD/CONVERSION FUNCTIONS ---

def download_and_convert_video(folder_path, artist, song_name, config):
    """Uses yt-dlp to search, download, and convert the video."""
    
    if os.path.exists(os.path.join(folder_path, "video.webm")):
        return False 
        
    print(f" -> Searching & Downloading video for: {artist} - {song_name}")
    
    query = f"ytsearch1:{artist} - {song_name} official video"
    output_path = os.path.join(folder_path, "video.webm")
    
    # --- GET CONFIG VALUES ---
    MAX_WIDTH = config['video'].get('max_width', DEFAULT_CONFIG['video']['max_width'])
    MAX_BITRATE = config['video'].get('max_bitrate', DEFAULT_CONFIG['video']['max_bitrate'])

    # === Conversion Flags ===
    # Using dynamic values read from config
    scaling = f"-vf scale={MAX_WIDTH}:-2" # Scales video down to max width
    encoding_flags = f"-c:v libvpx -b:v {MAX_BITRATE} -c:a libvorbis -quality good -speed 8 -threads 0"
    
    conversion_args = f"{scaling} {encoding_flags}"
    
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
        # CLEANED: Removed speed/stability mention
        print(" -> Download and Conversion Complete.")
        return True
    except subprocess.CalledProcessError as e:
        print(f" -> ERROR: Download/Conversion failed for {artist} - {song_name}. (Code: {e.returncode})")
        return False
    except FileNotFoundError:
        print(" -> ERROR: yt-dlp.exe or ffmpeg.exe not found in utility folder!")
        sys.exit(1)


def process_songs_folder(songs_path):
    """Iterates through all song folders to download missing videos."""
    config = get_config()
    current_res = config['video'].get('max_width', DEFAULT_CONFIG['video']['max_width'])
    current_br = config['video'].get('max_bitrate', DEFAULT_CONFIG['video']['max_bitrate'])
    
    downloaded_count = 0
    # CLEANED: Removed speed/stability mention
    print("--- Starting Automatic Video Search and Download ---")
    print(f"--- Current Max Resolution Width: {current_res} | Max Bitrate: {current_br} ---")
    
    # Use os.walk to recursively find all subfolders
    for root, dirs, files in os.walk(songs_path):
        # Check if the current directory is a song folder (i.e., contains song.ini or notes.chart)
        if 'song.ini' in files or 'notes.chart' in files:
            artist, name = get_song_metadata(root)
            
            if artist and name and not artist == 'Unknown':
                if download_and_convert_video(root, artist, name, config):
                    downloaded_count += 1
            else:
                print(f"Skipping folder '{Path(root).name}': Could not find Artist/Name metadata.")

    print(f"\n--- Download Summary ---")
    print(f"Total new videos downloaded and converted: {downloaded_count}")
    return downloaded_count

# --- MAIN EXECUTION LOGIC ---
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Usage: python auto_downloader.py <path_to_songs_folder> or python auto_downloader.py --config <key> <value>")
        sys.exit(1)
        
    # CONFIGURATION SET MODE (Used by BAT menu option 6)
    if sys.argv[1] == '--set-config' and len(sys.argv) == 4:
        key = sys.argv[2]
        value = sys.argv[3]
        
        config = get_config()
        
        if 'video' not in config or key not in config['video']:
             print(f"ERROR: Invalid configuration key '{key}'. Valid keys are: {', '.join(DEFAULT_CONFIG['video'].keys())}")
             sys.exit(1)

        # Basic validation for resolution/width
        if key == 'max_width':
            try:
                int_val = int(value)
                if int_val < 640:
                    print("Warning: Resolution width is too low. Using 640 as minimum.")
                    value = '640'
                config['video'][key] = str(int(value))
            except ValueError:
                print(f"ERROR: Max resolution width must be an integer. Received: {value}")
                sys.exit(1)
        # Basic validation for bitrate
        elif key == 'max_bitrate':
            if not re.match(r'^\d+(\.\d+)?[kKmMgG]$', value):
                 print(f"ERROR: Max bitrate must be a value like 1.5M or 2000k. Received: {value}")
                 sys.exit(1)
            config['video'][key] = value
        
        save_config(config)
        print(f"SUCCESS: Configuration updated. {key} set to {value}")
        sys.exit(0)
        
    # CONFIGURATION GET MODE (Used by BAT to retrieve values)
    elif sys.argv[1] == '--get-config' and len(sys.argv) == 3:
        key = sys.argv[2]
        config = get_config()
        # Print the value or the default if the key is missing
        print(config['video'].get(key, DEFAULT_CONFIG['video'].get(key)))
        sys.exit(0)
        
    # DOWNLOAD MODE
    else:
        songs_folder_path = sys.argv[1]
        
        if not os.path.isdir(songs_folder_path):
            print(f"Error: Folder not found at {songs_folder_path}")
            sys.exit(1)
            
        process_songs_folder(songs_folder_path)