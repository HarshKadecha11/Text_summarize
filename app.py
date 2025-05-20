# app.py
import nltk
import heapq
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def download_nltk_resources():
    """Download required NLTK resources."""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading necessary NLTK resources...")
        nltk.download('punkt')
        nltk.download('stopwords')

# Download resources on startup
download_nltk_resources()

def preprocess_text(text):
    """Clean and preprocess the input text."""
    # Remove special characters and numbers
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = text.strip()
    text = text.lower()
    return text

def extract_summary(text, num_sentences=5):
    """
    Extract a summary from text using frequency-based ranking.
    
    Args:
        text (str): The input text to summarize
        num_sentences (int): Number of sentences to include in summary
        
    Returns:
        str: A concise summary of the input text
        dict: Statistics about the summarization
    """
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    
    # If text is too short, return it as is
    if len(sentences) <= num_sentences:
        return text, {
            "original_chars": len(text),
            "original_words": len(text.split()),
            "original_sentences": len(sentences),
            "summary_chars": len(text),
            "summary_words": len(text.split()),
            "summary_sentences": len(sentences),
            "reduction_percent": 0
        }
    
    # Preprocess text and calculate word frequencies
    processed_text = preprocess_text(text)
    stop_words = set(stopwords.words('english'))
    
    word_frequencies = {}
    for word in word_tokenize(processed_text):
        if word not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    # Normalize word frequencies
    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if i not in sentence_scores:
                    sentence_scores[i] = word_frequencies[word]
                else:
                    sentence_scores[i] += word_frequencies[word]
    
    # Get top N sentences
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores.items(), key=lambda x: x[1])
    summary_sentences = [sentences[i] for i, _ in sorted(summary_sentences, key=lambda x: x[0])]
    
    # Join sentences to form summary
    summary = ' '.join(summary_sentences)
    
    # Calculate statistics
    stats = {
        "original_chars": len(text),
        "original_words": len(text.split()),
        "original_sentences": len(sentences),
        "summary_chars": len(summary),
        "summary_words": len(summary.split()),
        "summary_sentences": len(summary_sentences),
        "reduction_percent": round(100 - (len(summary) / len(text) * 100), 1)
    }
    
    return summary, stats

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    num_sentences = data.get('sentences', 5)
    
    try:
        num_sentences = int(num_sentences)
    except ValueError:
        num_sentences = 5
    
    if not text.strip():
        return jsonify({
            'error': 'No text provided'
        }), 400
    
    summary, stats = extract_summary(text, num_sentences)
    
    return jsonify({
        'summary': summary,
        'stats': stats
    })

if __name__ == '__main__':
    app.run(debug=True)