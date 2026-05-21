#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python packages
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create downloads directory (just in case)
mkdir -p downloads

# Download ffmpeg static build for Linux (amd64)
echo "Installing FFmpeg..."
curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
mkdir -p ffmpeg_temp
tar -xJf ffmpeg.tar.xz -C ffmpeg_temp --strip-components=1
cp ffmpeg_temp/ffmpeg ffmpeg_temp/ffprobe .
chmod +x ffmpeg ffprobe
rm -rf ffmpeg.tar.xz ffmpeg_temp
echo "FFmpeg installed successfully!"
