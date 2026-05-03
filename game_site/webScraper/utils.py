import requests
from bs4 import BeautifulSoup

def scrape_reviews(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    titles = [h2.text.strip() for h2 in soup.select("h2.review-title")]
    scores = [s.text.strip() for s in soup.select(".score")]
    links = [a["href"] for a in soup.select("a.review-link")]

    return list(zip(titles, scores, links))