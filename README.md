Project Overview

This project is a Python-based web scraping and data-processing pipeline that collects data from multiple public websites, cleans and standardizes the data, validates the records, detects duplicates, and generates a consolidated dataset.

Data Sources

•	Books to Scrape

•	Quotes to Scrape

Technology Used

•	Python

•	Requests

•	BeautifulSoup

•	Pandas

•	Pytest

Processing Flow

Websites → Scraping → Cleaning → Validation → Deduplication → Consolidation → Output

The pipeline handles pagination, parsing errors, invalid records, and duplicate data. The final processed data is saved as a CSV file, while execution metrics and processing statistics are stored in a JSON summary report. Logs are also maintained for monitoring and troubleshooting.

Outputs
<img width="974" height="513" alt="image" src="https://github.com/user-attachments/assets/8c0a0d82-720b-4a04-9b2f-3e7f6c4e71cf" />
<img width="975" height="564" alt="image" src="https://github.com/user-attachments/assets/35417f85-4c95-491f-8f0a-90eb1838be40" />

•	output/final_dataset.csv — Consolidated cleaned dataset

<img width="975" height="418" alt="image" src="https://github.com/user-attachments/assets/9118f870-6248-4df3-91ee-2566d3f57c4f" />

•	output/summary_report.json — Processing and quality metrics

<img width="796" height="561" alt="image" src="https://github.com/user-attachments/assets/567c8ff4-4ed7-4db6-9e4b-ac916f1506fd" />

•	logs/scraper.log — Execution logs

<img width="975" height="534" alt="image" src="https://github.com/user-attachments/assets/a501ecd8-d9ee-4d44-8a50-070e13170214" />
