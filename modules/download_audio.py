import yt_dlp
import os

def download_audio_from_youtube(yt_url, output_path="data/output/podcast_audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    print(f"Audio downloaded and saved to {output_path}")
