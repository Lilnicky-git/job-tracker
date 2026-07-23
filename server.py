import os

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

ADZUNA_APP_ID = os.environ["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = os.environ["ADZUNA_APP_KEY"]

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


if __name__ == "__main__":
    mcp.run()
