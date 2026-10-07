import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging


BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_books():
    books = []
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

            book_cards = soup.select("article.product_pod")

            for book in book_cards:
                try:
                    title_element = book.select_one("h3 a")
                    price_element = book.select_one(".price_color")
                    availability_element = book.select_one(
                        ".availability"
                    )
                    rating_element = book.select_one("p.star-rating")

                    title = (
                        title_element.get("title", "").strip()
                        if title_element
                        else ""
                    )

                    price = (
                        price_element.get_text(strip=True)
                        if price_element
                        else ""
                    )

                    availability = (
                        availability_element.get_text(" ", strip=True)
                        if availability_element
                        else ""
                    )

                    rating = (
                        rating_element.get("class", [])
                        if rating_element
                        else []
                    )

                    rating = next(
                        (
                            value
                            for value in rating
                            if value in [
                                "One",
                                "Two",
                                "Three",
                                "Four",
                                "Five"
                            ]
                        ),
                        ""
                    )

                    relative_url = (
                        title_element.get("href")
                        if title_element
                        else ""
                    )

                    product_url = (
                        urljoin(current_url, relative_url)
                        if relative_url
                        else ""
                    )

                    books.append({
                        "source": "Books to Scrape",
                        "source_url": product_url,
                        "name_or_title": title,
                        "category": "",
                        "price": price,
                        "rating": rating,
                        "author": "",
                        "tags": "",
                        "description": "",
                        "availability": availability
                    })

                except Exception as error:
                    logging.warning(
                        f"Failed to parse a book: {error}"
                    )

            # Find next page
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

            # Stop this source but allow other sources to run
            break

        except Exception as error:
            logging.error(
                f"Unexpected error on {current_url}: {error}"
            )
            break

    logging.info(
        f"Books scraped successfully: {len(books)}"
    )

    return books