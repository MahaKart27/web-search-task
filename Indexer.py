import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import re
import nltk
from nltk.corpus import stopwords

class Indexer:
    def __init__(self):
        self.index = defaultdict(list)
        nltk.download('stopwords')  # Download stopwords if not already downloaded

    def index_page(self, url, text_content):
        tokens = self.tokenize_text(text_content)
        tokens = self.remove_stop_words(tokens)
        # Store the indexed information along with the URL
        for token in tokens:
            self.index[token].append({'url': url, 'content': text_content})

    def tokenize_text(self, text):
        # Tokenize text
        return re.findall(r'\b\w+\b', text.lower())

    def remove_stop_words(self, tokens):
        # Remove NLTK English stopwords
        stop_words = set(stopwords.words('english'))
        return [token for token in tokens if token not in stop_words]

def main():
    indexer = Indexer()

if __name__ == "__main__":
    main()
