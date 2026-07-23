import os
import sqlite3

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

ADZUNA_APP_ID = os.environ["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = os.environ["ADZUNA_APP_KEY"]

db = sqlite3.connect("tracker.db", check_same_thread=False)
db.execute("PRAGMA foreign_keys = ON")

mcp = FastMCP("job-tracker")


@mcp.tool()
def search_jobs(keywords: str, location: str = "New York") -> list[dict]:
    """Search Adzuna for job postings matching keywords and a location."""
    response = requests.get(
        "https://api.adzuna.com/v1/api/jobs/us/search/1",
        params={
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": keywords,
            "where": location,
            "results_per_page": 10,
        },
    )
    response.raise_for_status()
    return [
        {
            "title": r["title"],
            "company": r.get("company", {}).get("display_name"),
            "location": r.get("location", {}).get("display_name"),
            "salary_min": r.get("salary_min"),
            "salary_max": r.get("salary_max"),
            "url": r.get("redirect_url"),
        }
        for r in response.json()["results"]
    ]


@mcp.tool()
def save_posting(
    company_name: str,
    title: str,
    location: str | None = None,
    salary_min: int | None = None,
    salary_max: int | None = None,
    source_url: str | None = None,
) -> dict:
    """Save a chosen job search result as a posting, creating the company if it doesn't exist yet."""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM companies WHERE name = ?", (company_name,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO companies (name) VALUES (?)", (company_name,))
        company_id = cursor.lastrowid
    else:
        company_id = row[0]

    cursor.execute(
        """INSERT INTO postings (company_id, title, location, salary_min, salary_max, source_url, date_found, status)
           VALUES (?, ?, ?, ?, ?, ?, date('now'), 'new')""",
        (company_id, title, location, salary_min, salary_max, source_url),
    )
    db.commit()
    return {"posting_id": cursor.lastrowid}


if __name__ == "__main__":
    mcp.run()
