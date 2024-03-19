import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import re
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download('stopwords')

class Ranker:
    def __init__(self, index):
        self.index = index
        self.stop_words = set(stopwords.words('english'))

    def search(self, query):
        query_tokens = self.tokenize_text(query)
        query_tokens = self.remove_stop_words(query_tokens)
        results = defaultdict(int)
        # Count occurrences of query tokens in indexed content
        for token in query_tokens:
            if token in self.index:
                for indexed_data in self.index[token]:
                    results[indexed_data['url']] += 1
        # Sort results by occurrence count (ranking)
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        return [url for url, _ in sorted_results]

    def tokenize_text(self, text):
        # Tokenize text
        return re.findall(r'\b\w+\b', text.lower())

    def remove_stop_words(self, tokens):
        # Remove common stop words using NLTK stopwords
        return [token for token in tokens if token not in self.stop_words]


def main():
    ranker = Ranker(indexer.index)


if __name__ == "__main__":
    main()
