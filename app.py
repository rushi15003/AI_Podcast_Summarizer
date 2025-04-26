from flask import Flask, render_template, request, send_file
import os
import yt_dlp as youtube_dl
import warnings
from gtts import gTTS

from modules.transcribe_audio import transcribe_audio
from modules.summarize_text import summarize_text
from modules.database import init_db, insert_podcast
from modules.recommendation import search_related_videos_tfidf

# Suppress warnings
warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)

# Initialize database
init_db(app)

# Output directory setup
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)  # For saving TTS audio file

def download_audio(youtube_url):
    """Download audio from a YouTube video and return the file path."""
    audio_file = os.path.join(OUTPUT_DIR, "podcast_audio.mp3")
    
    if os.path.exists(audio_file):
        os.remove(audio_file)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(OUTPUT_DIR, "podcast_audio.%(ext)s"),
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        for file in os.listdir(OUTPUT_DIR):
            if file.startswith("podcast_audio") and file.endswith(".mp3"):
                downloaded_audio_file = os.path.join(OUTPUT_DIR, file)
                os.rename(downloaded_audio_file, audio_file)
                break
        
        if not os.path.exists(audio_file):
            raise FileNotFoundError("❌ Audio file was not downloaded properly.")
        return audio_file
    except Exception:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_podcast', methods=['POST'])
def process_podcast():
    """Handles the podcast transcription and summarization process."""
    try:
        youtube_url = request.form.get('youtube_url')
        if not youtube_url:
            return "❌ Please provide a valid YouTube URL."

        audio_file_path = download_audio(youtube_url)
        if not audio_file_path:
            return "❌ Failed to download audio."

        # Transcribe audio
        transcription, detected_lang = transcribe_audio(audio_file_path)

        if transcription:
            summary = summarize_text(transcription)

            # Store results in the database
            success = insert_podcast(youtube_url, transcription, summary, detected_lang)
            if not success:
                return "Database error."

            # Generate TTS audio from summary
            tts = gTTS(text=summary, lang='en')
            tts_audio_path = os.path.join(STATIC_DIR, "summary_audio.mp3")
            tts.save(tts_audio_path)

            # Get recommended videos using TF-IDF
            recommendations = search_related_videos_tfidf(transcription)

            return render_template(
                'results.html', 
                transcription=transcription, 
                summary=summary, 
                language=detected_lang, 
                recommendations=recommendations,
                audio_path=tts_audio_path
            )
        else:
            return "❌ Transcription failed."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@app.route('/play-audio')
def play_audio():
    return send_file("static/summary_audio.mp3")
    
if __name__ == '__main__':
    app.run(debug=True)
