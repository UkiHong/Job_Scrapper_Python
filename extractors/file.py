from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


def save_to_file(jobs_db, keyword):
    file = open(f"{keyword}_jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(
        [
            "Title",
            "Company",
            "Location",
            "Reward",
            "Link",
        ]
    )

    for job in jobs_db:
        writer.writerow(job.values())

    file.close()
