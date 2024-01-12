import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_project_links(url, base_url="https://github.com/"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/eddycy92/SAHAssistant'):
                full_url = urljoin(base_url, href)
                print(full_url)

# Replace with the main URL of your project
extract_project_links("https://github.com/eddycy92/SAHAssistant")
