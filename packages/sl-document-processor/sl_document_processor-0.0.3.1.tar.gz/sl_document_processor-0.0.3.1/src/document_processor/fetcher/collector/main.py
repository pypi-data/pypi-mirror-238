
import logging
import requests

from pydantic import BaseModel
from bs4 import BeautifulSoup


class URLConfig(BaseModel):
    url: str
    max_depth: int = 1
    suffix: str = '.pdf'
    process_static_pages: bool = False

class URLCollector:
    def __init__(self, url_info: URLConfig):
        self.url = url_info.url
        self.max_depth = url_info.max_depth
        self.suffix = url_info.suffix
        self.process_static_pages = url_info.process_static_pages

    def _collect_urls_from_static_pages(self):
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.find_all('a', href=True)

            pdf_links = []

            for link in links:
                if link['href'].endswith(self.suffix):
                    pdf_links.append(link['href'])
            
            return pdf_links
        except requests.exceptions.RequestException as e:
            logging.debug("Error: %s", e)
            return []

    def collect_urls(self):
        if self.process_static_pages:
            return self._collect_urls_from_static_pages()

