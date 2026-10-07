import re
import unicodedata


def normalize_for_comparison(value):
    if value is None:
        return ""
    value = str(value)
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\s+", " ", value)
    value = value.strip()
    value = value.lower()
    return value


def create_duplicate_key(record):
    source = normalize_for_comparison(
        record.get("source")
    )
    name_or_title = normalize_for_comparison(
        record.get("name_or_title")
    )
    return f"{source}|{name_or_title}"


def deduplicate_records(records):
    seen = set()
    unique_records = []
    duplicate_records = []
    for record in records:
        duplicate_key = create_duplicate_key(record)
        if duplicate_key in seen:
            duplicate_records.append(record)
        else:
            seen.add(duplicate_key)
            unique_records.append(record)
    return unique_records, duplicate_records