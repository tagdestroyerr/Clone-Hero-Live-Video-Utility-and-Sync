import sys
import subprocess
import os

def run_conversion(input_path, output_path, max_w, max_br, is_download=False, url=None):
    """
    Executes yt-dlp (Option 1) or ffmpeg (Option 3) reliably.
    """
    try:
        if is_download:
            # Command for Option 1 (Manual Download)
            command = [
                'yt-dlp.exe',
                '-f', 'bestvideo+bestaudio/best',
                '--ffmpeg-location', 'ffmpeg.exe',
                '--recode-video', 'webm',
                '--postprocessor-args', f'-vf scale={max_w}:-2 -c:v libvpx -b:v {max_br} -c:a libvorbis -quality good -speed 8 -threads 0',
                '-o', output_path,
                url
            ]
        else:
            # Command for Option 3 (Convert Existing MP4)
            command = [
                'ffmpeg.exe',
                '-i', input_path,
                '-vf', f'scale={max_w}:-2',
                '-c:v', 'libvpx',
                '-b:v', max_br,
                '-c:a', 'libvorbis',
                '-y',
                output_path
            ]
        
        # Run the command and capture output
        print(f"Executing command: {' '.join(command)}")
        
        # Use subprocess.run for direct, reliable execution
        result = subprocess.run(
            command,
            check=True,  # Raise an exception for non-zero exit code
            cwd=os.path.dirname(os.path.abspath(__file__)) # Execute from script directory
        )
        
        print("External program finished successfully.")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: External program failed with code {e.returncode}")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Output: {e.output}")
        return 1
    except FileNotFoundError:
        print("\nERROR: Executable (ffmpeg.exe or yt-dlp.exe) not found.")
        return 1
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_processor.py <mode> [args...]")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "download" and len(sys.argv) == 6:
        # download <url> <output_path> <max_w> <max_br>
        url, output_path, max_w, max_br = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        sys.exit(run_conversion(None, output_path, max_w, max_br, is_download=True, url=url))
        
    elif mode == "convert" and len(sys.argv) == 6:
        # convert <input_path> <output_path> <max_w> <max_br>
        input_path, output_path, max_w, max_br = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        sys.exit(run_conversion(input_path, output_path, max_w, max_br))
        
    else:
        print(f"Invalid arguments for mode: {mode}")
        sys.exit(1)