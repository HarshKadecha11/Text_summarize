# SmartSummarize - AI-Powered Article Summarizer

SmartSummarize is a web application that automatically generates concise summaries from longer texts using natural language processing techniques. The application extracts the most important sentences from the input text to create a coherent summary.

## Features

- **Text Summarization**: Automatically extract key sentences from lengthy text
- **Customizable Summary Length**: Control how many sentences to include in the summary
- **Analytics Dashboard**: View statistics about the original text and the generated summary
- **Responsive Design**: Works on desktop and mobile devices
- **Copy to Clipboard**: Easily copy the generated summary

## Technology Stack

- **Backend**: Python with Flask
- **NLP Processing**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML, CSS, JavaScript

## How It Works

The application uses an extractive summarization technique based on word frequency analysis:

1. **Text Preprocessing**: Removes special characters, numbers, and stopwords
2. **Sentence Tokenization**: Splits the text into individual sentences
3. **Word Frequency Analysis**: Calculates the importance of each word in the text
4. **Sentence Scoring**: Scores sentences based on the importance of their constituent words
5. **Summary Generation**: Selects top-scoring sentences while preserving their original order

## Installation

### Prerequisites

- Python 3.7+ 
- pip package manager

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/text_summarize.git
   cd text_summarize
   ```

2. Install the required dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Enter or paste your text in the input field
2. Adjust the number of sentences you want in your summary using the slider
3. Click "Summarize Text" to generate the summary
4. View the summary and statistics about the original text and generated summary
5. Use the copy button to copy the summary to your clipboard



## Dependencies

- Flask: Web framework
- NLTK: Natural language processing library
- Regex: Text cleaning and preprocessing

## License

[MIT License](LICENSE)

## Acknowledgments

- [NLTK](https://www.nltk.org/) for providing the natural language processing tools
- [Flask](https://flask.palletsprojects.com/) for the web framework