import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import re

class Ranker:
    def __init__(self, index):
        self.index = index

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
        # Remove common stop words (this can be expanded)
        stop_words = {'a', 'an', 'the', 'is', 'are', 'and', 'or', 'not'}
        return [token for token in tokens if token not in stop_words]


def main():
    ranker = Ranker(indexer.index)


if __name__ == "__main__":
    main()