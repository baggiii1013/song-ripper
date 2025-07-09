#!/usr/bin/env python3
"""
YouTube Audio Downloader and FLAC Converter
============================================

This script downloads audio from YouTube URLs using yt-dlp and converts them to FLAC format using FFmpeg.

Requirements:
- yt-dlp: for downloading YouTube audio
- ffmpeg: for audio conversion (must be installed on system)

Usage:
    python youtube_to_flac.py
    
Then paste the YouTube URL when prompted.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
import tempfile
import shutil

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def check_dependencies():
    """Check if required dependencies are available"""
    print_colored("🔍 Checking dependencies...", Colors.CYAN)
    
    # Check yt-dlp
    try:
        import yt_dlp
        print_colored("✅ yt-dlp is installed", Colors.GREEN)
    except ImportError:
        print_colored("❌ yt-dlp is not installed. Please run: pip install yt-dlp", Colors.RED)
        return False
    
    # Check ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        print_colored("✅ ffmpeg is installed", Colors.GREEN)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("❌ ffmpeg is not installed. Please install ffmpeg on your system", Colors.RED)
        return False

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    youtube_patterns = [
        r'^https?://(www\.)?(youtube\.com|youtu\.be)/',
        r'^https?://m\.youtube\.com/',
        r'^https?://music\.youtube\.com/'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters for filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Remove leading/trailing underscores and dots
    filename = filename.strip('_.')
    
    return filename

def download_audio(url, output_dir):
    """Download audio from YouTube URL using yt-dlp"""
    print_colored(f"📥 Downloading audio from: {url}", Colors.YELLOW)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best quality audio
        'extractaudio': True,        # Extract audio only
        'audioformat': 'best',       # Keep original audio format
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),  # Output filename template
        'noplaylist': True,          # Don't download playlists
        'writethumbnail': False,     # Don't download thumbnails
        'writeinfojson': False,      # Don't write info JSON
        'ignoreerrors': False,       # Stop on errors
    }
    
    try:
        import yt_dlp
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print_colored(f"📋 Title: {title}", Colors.BLUE)
            if duration:
                minutes = duration // 60
                seconds = duration % 60
                print_colored(f"⏱️  Duration: {minutes}:{seconds:02d}", Colors.BLUE)
            
            # Download the audio
            ydl.download([url])
            
            # Find the downloaded file
            downloaded_files = []
            for file in output_path.glob('*'):
                if file.is_file() and file.name.startswith(sanitize_filename(title)):
                    downloaded_files.append(file)
            
            if downloaded_files:
                # Return the most recently created file
                return max(downloaded_files, key=lambda f: f.stat().st_ctime)
            else:
                print_colored("❌ Could not find downloaded file", Colors.RED)
                return None
                
    except Exception as e:
        print_colored(f"❌ Error downloading audio: {str(e)}", Colors.RED)
        return None

def convert_to_flac(input_file, output_dir):
    """Convert audio file to FLAC format using ffmpeg"""
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create output filename with .flac extension
    output_filename = input_path.stem + '.flac'
    output_file = output_path / output_filename
    
    print_colored(f"🔄 Converting to FLAC: {output_filename}", Colors.YELLOW)
    
    try:
        # FFmpeg command to convert to FLAC with high quality
        cmd = [
            'ffmpeg',
            '-i', str(input_path),      # Input file
            '-acodec', 'flac',          # Use FLAC codec
            '-compression_level', '8',   # Maximum compression
            '-y',                       # Overwrite output file if it exists
            str(output_file)            # Output file
        ]
        
        # Run ffmpeg conversion
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print_colored(f"✅ Successfully converted to FLAC: {output_file}", Colors.GREEN)
        
        # Remove the original downloaded file
        try:
            input_path.unlink()
            print_colored(f"🗑️  Removed original file: {input_path.name}", Colors.CYAN)
        except Exception as e:
            print_colored(f"⚠️  Could not remove original file: {str(e)}", Colors.YELLOW)
        
        return output_file
        
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error converting to FLAC: {e.stderr}", Colors.RED)
        return None
    except Exception as e:
        print_colored(f"❌ Unexpected error during conversion: {str(e)}", Colors.RED)
        return None

def get_file_size(file_path):
    """Get human-readable file size"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def main():
    """Main function"""
    print_colored("🎵 YouTube Audio Downloader & FLAC Converter", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 50, Colors.MAGENTA)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get YouTube URL from user
    print_colored("\n📎 Please paste the YouTube URL:", Colors.CYAN)
    url = input("> ").strip()
    
    if not url:
        print_colored("❌ No URL provided", Colors.RED)
        sys.exit(1)
    
    if not is_valid_youtube_url(url):
        print_colored("❌ Invalid YouTube URL", Colors.RED)
        sys.exit(1)
    
    # Set up output directories
    script_dir = Path(__file__).parent
    downloads_dir = script_dir / 'downloads'
    flac_dir = script_dir / 'flac_output'
    
    try:
        # Download audio
        downloaded_file = download_audio(url, downloads_dir)
        
        if not downloaded_file:
            print_colored("❌ Failed to download audio", Colors.RED)
            sys.exit(1)
        
        print_colored(f"📁 Downloaded: {downloaded_file.name}", Colors.GREEN)
        print_colored(f"📊 Size: {get_file_size(downloaded_file)}", Colors.BLUE)
        
        # Convert to FLAC
        flac_file = convert_to_flac(downloaded_file, flac_dir)
        
        if flac_file:
            print_colored(f"\n🎉 SUCCESS! FLAC file created:", Colors.BOLD + Colors.GREEN)
            print_colored(f"📁 Location: {flac_file}", Colors.GREEN)
            print_colored(f"📊 Size: {get_file_size(flac_file)}", Colors.BLUE)
        else:
            print_colored("❌ Failed to convert to FLAC", Colors.RED)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Process interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"❌ Unexpected error: {str(e)}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
