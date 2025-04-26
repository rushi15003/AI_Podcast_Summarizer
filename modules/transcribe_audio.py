import whisper
import torch
from transformers import pipeline

# def transcribe_audio(audio_path):
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = whisper.load_model("base").to(device)
#
#     result = model.transcribe(audio_path)
#
#     print("Transcription:\n", result["text"])
#     return result["text"]

def transcribe_audio(audio_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisper.load_model("base").to(device)
    result = model.transcribe(audio_path)

    detected_language = result["language"]
    transcription = result["text"]
    print(f"Detected language: {detected_language}")
    print("Original Transcription:\n", transcription)

    # Translate to English if the detected language is not English
    if detected_language != "en":
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
        # Split the text into chunks to avoid exceeding max token limit
        chunk_size = 20
        chunks = [transcription[i:i+chunk_size] for i in range(0, len(transcription), chunk_size)]
        translated_chunks = [translator(chunk)[0]['translation_text'] for chunk in chunks]
        transcription = ' '.join(translated_chunks)
        print("Translated Transcription:\n", transcription)

    return transcription, detected_language
