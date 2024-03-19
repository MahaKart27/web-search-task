import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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

