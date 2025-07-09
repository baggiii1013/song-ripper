# YouTube Audio Downloader & FLAC Converter

A Python script that downloads audio from YouTube URLs using `yt-dlp` and converts them to high-quality FLAC format using FFmpeg.

## Features

- 🎵 Download highest quality audio from YouTube
- 🔄 Convert to FLAC format with maximum compression
- 📁 Organized output directories
- 🎨 Colorful terminal output
- ✅ Dependency checking
- 🛡️ Error handling and validation
- 📊 File size information

## Requirements

### System Dependencies
- **FFmpeg** - Must be installed on your system
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org/

### Python Dependencies
- **yt-dlp** - For downloading YouTube audio

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the script:**
   ```bash
   python youtube_to_flac.py
   ```

3. **Paste the YouTube URL when prompted**

## Output Structure

```
song-ripper/
├── downloads/          # Temporary download files (auto-cleaned)
├── flac_output/        # Final FLAC files
├── venv/              # Virtual environment
├── youtube_to_flac.py # Main script
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Supported URLs

- https://www.youtube.com/watch?v=...
- https://youtu.be/...
- https://m.youtube.com/...
- https://music.youtube.com/...

## Features in Detail

### Audio Quality
- Downloads the highest quality audio available
- Converts to FLAC with maximum compression (level 8)
- Preserves original audio quality

### File Management
- Automatically sanitizes filenames
- Removes temporary files after conversion
- Creates organized output directories

### Error Handling
- Validates YouTube URLs
- Checks for required dependencies
- Handles network errors gracefully
- Provides informative error messages

## Troubleshooting

### Common Issues

1. **"yt-dlp is not installed"**
   - Make sure you're in the virtual environment
   - Run: `pip install yt-dlp`

2. **"ffmpeg is not installed"**
   - Install FFmpeg on your system (see Requirements section)

3. **"Invalid YouTube URL"**
   - Check that the URL is a valid YouTube link
   - Make sure the URL is accessible

4. **Download fails**
   - Check your internet connection
   - Some videos may be region-restricted
   - Try a different video

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
