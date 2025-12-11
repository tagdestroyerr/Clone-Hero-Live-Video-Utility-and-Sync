import sys
import os
import re
from pathlib import Path # Required for the Path object

def sync_ini(songs_folder):
    """
    Recursively scans song folders for 'song.ini', ensures 'video = video.webm' 
    is present if the video file exists, and updates 'video_start_time' 
    to match the 'Gap' value for synchronization.
    """
    ini_files_synced = 0
    
    print("--- Starting INI File Repair and Synchronization ---")
    
    # Use os.walk for recursive traversal
    for root, _, files in os.walk(songs_folder):
        ini_path = os.path.join(root, 'song.ini')
        
        if os.path.exists(ini_path):
            gap_ms = 0
            video_start_time_found = False
            video_entry_found = False
            
            # FIX: Correctly join the path components using Path()
            video_file_exists = (Path(root) / 'video.webm').exists() 
            
            try:
                # 1. Read the file content
                with open(ini_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 2. Scan lines to find Gap and check for existing tags
                updated_lines = []
                current_section = None
                
                # Regex patterns (case-insensitive for keys)
                gap_regex = re.compile(r"^\s*Gap\s*=\s*(-?\d+(\.\d+)?)\s*$", re.IGNORECASE)
                video_start_time_regex = re.compile(r"^\s*video_start_time\s*=\s*(-?\d+)\s*$", re.IGNORECASE)
                video_entry_regex = re.compile(r"^\s*video\s*=\s*(.*)\s*$", re.IGNORECASE) # Catch any video entry
                section_regex = re.compile(r"^\[([a-zA-Z0-9_]+)\]\s*$")
                
                print(f"\n[Checking: {Path(root).name}]")

                for line in lines:
                    line_stripped = line.strip()
                    
                    # Detect section headers
                    section_match = section_regex.match(line_stripped)
                    if section_match:
                        current_section = section_match.group(1).lower()
                    
                    if current_section == 'song':
                        # Find Gap value
                        gap_match = gap_regex.match(line_stripped)
                        if gap_match:
                            gap_ms = int(float(gap_match.group(1)))

                        # Check for existing video_start_time (and skip it for replacement)
                        if video_start_time_regex.match(line_stripped):
                            video_start_time_found = True
                            continue # Skip the old line

                        # Check for existing video = [file] entry
                        if video_entry_regex.match(line_stripped):
                            video_entry_found = True
                            
                    updated_lines.append(line)

                # 3. Determine where to insert/update the required lines
                
                if (video_file_exists and not video_entry_found) or video_start_time_found or gap_ms != 0:
                    
                    print(f" -> Found Gap: {gap_ms}ms")
                    
                    # Find the insertion point (right after [Song] header)
                    try:
                        song_section_index = next(i for i, line in enumerate(updated_lines) if line.strip().lower() == '[song]')
                        insertion_index = song_section_index + 1
                    except StopIteration:
                        # Fallback: If [Song] section is missing, append it
                        updated_lines.append('\n[Song]\n')
                        insertion_index = len(updated_lines)
                    
                    
                    # A. Insert video = video.webm if video exists and the tag is missing
                    if video_file_exists and not video_entry_found:
                         updated_lines.insert(insertion_index, f'video = video.webm\n')
                         print(" -> Added: video = video.webm (FIXED LOAD ERROR)")
                         insertion_index += 1
                        
                    # B. Insert the corrected video_start_time
                    if video_start_time_found or gap_ms != 0:
                        updated_lines.insert(insertion_index, f'video_start_time = {gap_ms}\n')
                        print(f" -> Set: video_start_time = {gap_ms} (FIXED SYNC)")
                        
                    # 4. Write the file back
                    with open(ini_path, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)
                    
                    ini_files_synced += 1
                else:
                    print(" -> No video found or no synchronization needed. Skipping.")
                    
            except Exception as e:
                print(f"Error processing {ini_path}: {e}")
                
    print(f"\n--- Sync Summary ---")
    print(f"Total song.ini files repaired/synchronized: {ini_files_synced}")
    return ini_files_synced

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sync_ini.py <path_to_songs_folder>")
        sys.exit(1)
        
    songs_folder_path = sys.argv[1]
    
    if not os.path.isdir(songs_folder_path):
        print(f"Error: Folder not found at {songs_folder_path}")
        sys.exit(1)
        
    sync_ini(songs_folder_path)