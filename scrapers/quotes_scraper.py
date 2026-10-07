import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging


BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_quotes():
    quotes = []
    current_url = BASE_URL

    while current_url:
        try:
            logging.info(f"Scraping: {current_url}")

            response = requests.get(
                current_url,
                headers=HEADERS,
                timeout=10
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            quote_blocks = soup.select("div.quote")

            for quote in quote_blocks:
                try:
                    text_element = quote.select_one("span.text")
                    author_element = quote.select_one("small.author")

                    tag_elements = quote.select("div.tags a.tag")

                    quote_text = (
                        text_element.get_text(strip=True)
                        if text_element
                        else ""
                    )

                    author = (
                        author_element.get_text(strip=True)
                        if author_element
                        else ""
                    )

                    tags = [
                        tag.get_text(strip=True)
                        for tag in tag_elements
                    ]

                    # Find the author page
                    author_link = (
                        author_element.find_parent("div")
                        .find("a")
                        if author_element
                        else None
                    )

                    author_url = (
                        urljoin(current_url, author_link["href"])
                        if author_link and author_link.get("href")
                        else ""
                    )

                    quotes.append({
                        "source": "Quotes to Scrape",
                        "source_url": current_url,
                        "name_or_title": quote_text,
                        "category": "",
                        "price": "",
                        "rating": "",
                        "author": author,
                        "tags": ", ".join(tags),
                        "description": "",
                        "author_url": author_url
                    })

                except Exception as error:
                    logging.warning(
                        f"Failed to parse a quote: {error}"
                    )

            # Pagination
            next_link = soup.select_one("li.next a")

            if next_link and next_link.get("href"):
                current_url = urljoin(
                    current_url,
                    next_link["href"]
                )
            else:
                current_url = None

        except requests.RequestException as error:
            logging.error(
                f"Request failed for {current_url}: {error}"
            )
            break

        except Exception as error:
            logging.error(
                f"Unexpected error on {current_url}: {error}"
            )
            break

    logging.info(
        f"Quotes scraped successfully: {len(quotes)}"
    )

    return quotes