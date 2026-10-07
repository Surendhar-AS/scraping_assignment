import re
from urllib.parse import urlparse

def clean_text(value):
    if value is None:
        return ""
    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def clean_price(value):
    if value is None or value == "":
        return None
    try:
        value = str(value)
        value = re.sub(r"[^0-9.]", "", value)
        return float(value) if value else None
    except (ValueError, TypeError):
        return None

def clean_rating(value):
    rating_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5
    }
    if value is None:
        return None
    value = clean_text(value).lower()
    return rating_map.get(value)

def clean_url(value):
    if not value:
        return ""
    value = str(value).strip()
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value
    return ""

def clean_tags(value):
    if not value:
        return ""
    if isinstance(value, list):
        value = ", ".join(value)
    return clean_text(value)


def clean_record(record):
    cleaned = {
        "source": clean_text(record.get("source")),
        "source_url": clean_url(record.get("source_url")),
        "name_or_title": clean_text(
            record.get("name_or_title")
        ),
        "category": clean_text(
            record.get("category")
        ),
        "price": clean_price(
            record.get("price")
        ),
        "rating": clean_rating(
            record.get("rating")
        ),
        "author": clean_text(
            record.get("author")
        ),
        "tags": clean_tags(
            record.get("tags")
        ),
        "description": clean_text(
            record.get("description")
        ),
        "scraped_at": record.get("scraped_at")
    }
    return cleaned

def clean_records(records):
    return [
        clean_record(record)
        for record in records
    ]