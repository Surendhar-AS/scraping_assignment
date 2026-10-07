from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape"
}

def is_valid_url(url):
    if not url:
        return False
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except Exception:
        return False

def validate_record(record):
    if record.get("source") not in VALID_SOURCES:
        return False, "Invalid source"
    if not record.get("name_or_title"):
        return False, "Missing name_or_title"
    if not is_valid_url(record.get("source_url")):
        return False, "Invalid source_url"
    price = record.get("price")
    if price is not None:
        if not isinstance(price, (int, float)):
            return False, "Price is not numeric"
        if price < 0:
            return False, "Price cannot be negative"

    rating = record.get("rating")
    if rating is not None:
        if not isinstance(rating, int):
            return False, "Rating is not an integer"

        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"
    return True, None


def validate_records(records):
    valid_records = []
    rejected_records = []
    for record in records:
        is_valid, reason = validate_record(record)
        if is_valid:
            valid_records.append(record)
        else:
            rejected_records.append({
                "record": record,
                "reason": reason
            })
    return valid_records, rejected_records