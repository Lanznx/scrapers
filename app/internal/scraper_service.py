import logging
import os
from typing import List
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
    TimeFilters,
    TypeFilters,
    ExperienceLevelFilters,
    OnSiteOrRemoteFilters,
    SalaryBaseFilters,
)

logging.basicConfig(level=logging.INFO)


def create_linkedin_scraper():
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Get chromedriver path from environment variable or use default
    chrome_executable_path = os.environ.get("CHROMEDRIVER_PATH", None)
    chrome_binary_location = os.environ.get("CHROME_BIN", None)
    
    logging.info(f"Chrome executable path: {chrome_executable_path}")
    logging.info(f"Chrome binary location: {chrome_binary_location}")
    
    return LinkedinScraper(
        chrome_executable_path=chrome_executable_path,
        chrome_binary_location=chrome_binary_location,
        chrome_options=chrome_options,
        headless=True,
        max_workers=1,
        slow_mo=1.3,
        page_load_timeout=40,
    )


async def scrape_linkedin_jobs(
    locations: List[str] = ["United States", "Europe", "Asia"],
    limit: int = 100,
    job_title: str = "software engineer",
) -> List[dict]:
    jobs_data = []

    def on_data(data: EventData):
        if "remote" in data.title.lower() or "remote" in data.description.lower():
            job_info = {
                "title": data.title,
                "company": data.company,
                "company_link": data.company_link,
                "date": data.date,
                "link": data.link,
                "description": data.description,
                "insights": {} if data.insights is None or isinstance(data.insights, list) else data.insights,
            }
            jobs_data.append(job_info)
            logging.info(
                f"Found remote job: {job_info['title']} at {job_info['company']}"
            )

    def on_error(error):
        logging.error(f"Error during scraping: {error}")

    def on_end():
        logging.info("Scraping completed")

    scraper = create_linkedin_scraper()

    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query=job_title,
            options=QueryOptions(
                locations=locations,
                apply_link=True,
                skip_promoted_jobs=True,
                limit=limit,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                    experience=[
                        ExperienceLevelFilters.ENTRY_LEVEL,
                        ExperienceLevelFilters.MID_SENIOR,
                    ],
                    base_salary=SalaryBaseFilters.SALARY_100K,
                ),
            ),
        )
    ]

    try:
        scraper.run(queries)
    finally:
        print("Scraping completed")

    return jobs_data
