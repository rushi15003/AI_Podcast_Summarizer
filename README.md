# 🎧 AI-Podcast Summarizer

**AI-Podcast Summarizer** is an open-source tool designed to generate clean and concise summaries from podcast. By processing uploaded links using state-of-the-art AI models, it helps users quickly understand the key points of long-form podcast content without listening to the entire episode.

## 📚 Table of Contents

- [Project Overview]
- [Key Features]
- [Technology Stack]
- [Getting Started]
- [Usage]
- [Contributing]
- [License]

## 🚀 Project Overview

AI-Podcast Summarizer transcribes spoken audio and passes it through an advanced language model to generate meaningful summaries. The project is designed to work entirely in the backend and does not store any intermediate files, ensuring a lightweight and fast experience.

### Key Features

- **Automatic Transcription**: Converts audio to text using open-source models.
- **Smart Summarization**: Generates clear summaries using advanced NLP techniques.
- **Fast & Stateless Processing**: Everything happens in-memory — no file storage.
- **Open-Source & Customizable**: Easy to modify and extend for other use cases.
- **Clean Output**: Provides a simple and user-friendly summary of lengthy audio.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Transcription**: OpenAI Whisper (on CPU/GPU)
- **Summarization**: Hugging Face Transformers (Facebook/LargeCNN)
- **Audio Processing**: FFmpeg

## 📝 Getting Started

### Prerequisites

- Python 3.8+
- `ffmpeg` installed and added to system path
- `pip` for Python package management

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rushi15003/AI_Podcast_Summarizer.git
   cd AI_Based_Podcast_Summarizer_Tool

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv/Scripts/activate

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run the Application**
   ```bash
   python app.py

## 🎉 Usage
- **Upload Podcast Link** : Provide a Link(e.g Youtube)
- **Processing**: The backend transcribes and summarizes the content.
- **Receive Output**: A clean text summary is returned instantly.
