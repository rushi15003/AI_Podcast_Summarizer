from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch
import os
from nltk import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt_tab')

# Load BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Initialize summarizer pipeline
summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer,
    num_beams=4,
    batch_size=4,
    truncation=True,
    device=-1
)

def split_by_sentences(text, max_words=850, overlap=2):
    sentences = sent_tokenize(text)
    
    if len(sentences) < 5:  # Short text directly as one chunk
        return [" ".join(sentences)]  

    chunks = []
    current_chunk = []
    current_word_count = 0

    for i, sentence in enumerate(sentences):
        sentence_word_count = len(word_tokenize(sentence))

        if current_word_count + sentence_word_count > max_words:
            while not sentences[i].endswith(('.', '?', '!')) and i < len(sentences) - 1:
                i += 1
                sentence_word_count += len(word_tokenize(sentences[i]))

            chunks.append(" ".join(current_chunk))
            current_chunk = sentences[max(0, i - overlap):i + 1]
            current_word_count = sum(len(word_tokenize(s)) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_text(transcription):
    if not transcription.strip():
        return "No transcription available for summarization."

    chunks = split_by_sentences(transcription)

    summaries = []
    for chunk in chunks:
        try:
            if len(chunks) == 1:  # For short content
                max_len, min_len = 100, 30
                prompt = (
                    f"Summarize this podcast in a clear, concise paragraph under 100 words. "
                    f"Focus only on key points — avoid excessive detail. "
                    f"Content:\n{chunk}"
                )
            else:  # For longer content
                max_len, min_len = 100, 5
                prompt = (
                    f"Summarize this podcast in a concise, clear format. "
                    f"Focus strictly on key points: "
                    f"Strictly summarize each chunk in only 1 sentence. Prioritize brevity over detail. "
                    f"- List only the most important questions and answers. "
                    f"- Include only major ideas and insights — skip minor details. "
                    f"- Strictly avoid excessive detail or repetitive points.\n"
                    f"Content:\n{chunk}"
                )

            # Pass adjusted length dynamically to summarizer
            summary_output = summarizer(
                chunk,
                max_length=max_len,
                min_length=min_len
            )[0]["summary_text"]

            summaries.append(summary_output)

        except Exception as e:
            print(f"Error during summarization: {e}")
            summaries.append("Error generating summary for this part.")

    combined_summary = "-".join(summaries)

    print(f"Final Summary:\n{combined_summary}")
    return combined_summary