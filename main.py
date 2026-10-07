import os
import json
import time
import logging
from datetime import datetime

import pandas as pd

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes

from processing.cleaning import clean_records
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


# --------------------------------------------------
# Configuration
# --------------------------------------------------

OUTPUT_DIR = "output"
LOG_DIR = "logs"

FINAL_DATASET = os.path.join(
    OUTPUT_DIR,
    "final_dataset.csv"
)

SUMMARY_REPORT = os.path.join(
    OUTPUT_DIR,
    "summary_report.json"
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "scraper.log"
)


# --------------------------------------------------
# Directory setup
# --------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# --------------------------------------------------
# Logging setup
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():

    start_time = time.time()

    logger.info("***********************************")
    logger.info("Scraping pipeline started")
    logger.info("***********************************")

    logger.info("Starting Books to Scrape...")

    try:
        books = scrape_books()
    except Exception as error:
        logger.error(
            f"Books scraper failed: {error}"
        )
        books = []

    logger.info(
        f"Books records collected: {len(books)}"
    )

    logger.info("Starting Quotes to Scrape...")

    try:
        quotes = scrape_quotes()
    except Exception as error:
        logger.error(
            f"Quotes scraper failed: {error}"
        )
        quotes = []

    logger.info(
        f"Quotes records collected: {len(quotes)}"
    )
    raw_records = books + quotes

    logger.info(
        f"Total raw records: {len(raw_records)}"
    )
    scraped_at = datetime.now().isoformat()

    for record in raw_records:
        record["scraped_at"] = scraped_at
    logger.info("Cleaning records...")

    cleaned_records = clean_records(raw_records)

    logger.info(
        f"Records after cleaning: "
        f"{len(cleaned_records)}"
    )
    logger.info("Validating records...")

    valid_records, rejected_records = (
        validate_records(cleaned_records)
    )

    logger.info(
        f"Valid records: {len(valid_records)}"
    )

    logger.info(
        f"Rejected records: "
        f"{len(rejected_records)}"
    )
    logger.info("Checking for duplicates...")

    unique_records, duplicate_records = (
        deduplicate_records(valid_records)
    )

    logger.info(
        f"Duplicate records: "
        f"{len(duplicate_records)}"
    )

    logger.info(
        f"Final unique records: "
        f"{len(unique_records)}"
    )
    columns = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at"
    ]

    dataframe = pd.DataFrame(
        unique_records,
        columns=columns
    )
    dataframe.to_csv(
        FINAL_DATASET,
        index=False,
        encoding="utf-8"
    )
    logger.info(
        f"Final dataset saved to {FINAL_DATASET}"
    )
    execution_time = round(
        time.time() - start_time,
        2
    )

    summary = {
        "execution_time_seconds": execution_time,

        "records_collected": {
            "Books to Scrape": len(books),
            "Quotes to Scrape": len(quotes),
            "total": len(raw_records)
        },

        "records_after_cleaning": len(
            cleaned_records
        ),

        "records_rejected": len(
            rejected_records
        ),

        "duplicates_detected": len(
            duplicate_records
        ),

        "final_record_count": len(
            unique_records
        ),

        "output_files": {
            "dataset": FINAL_DATASET,
            "summary": SUMMARY_REPORT,
            "log": LOG_FILE
        }
    }

    with open(
        SUMMARY_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )
    logger.info(f"Summary report saved to {SUMMARY_REPORT}")
    logger.info("***********************************")
    logger.info("Scraping pipeline completed")
    logger.info(f"Execution time: {execution_time} seconds")
    logger.info("***********************************")


if __name__ == "__main__":
    main()