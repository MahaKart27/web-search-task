# Gherkin Scenario:
# Scenario: User searches within a specific website
# Given the user is on the search app
# When the user enters the URL of a particular website 
# And the user has been asked to give a keyword after typing the search URL.
# And executes a search query within that specific site
# Then the app should display all the URLs that contain keywords
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

# Gherkin Scenario:
# Scenario: Highlighting important part of the website in search results
# Given the user has entered a search query
# When the app displays the search results
# Then the app should highlight the important part in the results of each website for better visibility

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


# Gherkin Scenario:
# Scenario: Providing relevant suggestions based on user search patterns
# Given the app has access to user search patterns
# When the user performs a search
# Then the app should implement AI algorithms to provide relevant suggestions based on the user's search patterns

class WebCrawler:
    def __init__(self, indexer, ranker):
        self.indexer = indexer
        self.ranker = ranker
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = self.get_text_content(soup)
            self.indexer.index_page(url, text_content)

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if urlparse(href).netloc:
                        href = urljoin(base_url or url, href)
                    if href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def get_text_content(self, soup):
        # Extract text content from HTML
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text()

    def search(self, query):
        return self.ranker.search(query)

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")

def main():
    indexer = Indexer()
    ranker = Ranker(indexer.index)
    crawler = WebCrawler(indexer, ranker)
    start_url = input("Enter starting URL: ")
    crawler.crawl(start_url)
    query = input("Enter search query: ")
    results = crawler.search(query)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
