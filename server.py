import os
import sqlite3
from pathlib import Path

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

ADZUNA_APP_ID = os.environ["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = os.environ["ADZUNA_APP_KEY"]

db = sqlite3.connect(BASE_DIR / "tracker.db", check_same_thread=False)
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


@mcp.tool()
def log_application(posting_id: int, notes: str = "") -> dict:
    """Log an application to a saved posting and mark that posting as matched."""
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO applications (posting_id, date_applied, stage, notes) VALUES (?, date('now'), 'applied', ?)",
        (posting_id, notes),
    )
    application_id = cursor.lastrowid
    cursor.execute("UPDATE postings SET status = 'matched' WHERE id = ?", (posting_id,))
    db.commit()
    return {"application_id": application_id}


@mcp.tool()
def log_communication(
    application_id: int,
    type: str,
    direction: str,
    summary: str,
    follow_up_required: bool = False,
) -> dict:
    """Log a communication for an application. If a follow-up is required, automatically creates a linked task."""
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO communications (application_id, date, type, direction, summary, follow_up_required)
           VALUES (?, date('now'), ?, ?, ?, ?)""",
        (application_id, type, direction, summary, follow_up_required),
    )
    communication_id = cursor.lastrowid

    if follow_up_required:
        cursor.execute(
            """INSERT INTO tasks (application_id, type, due_date, status, notes)
               VALUES (?, 'follow_up', date('now', '+7 days'), 'open', ?)""",
            (application_id, f"Follow up on: {summary}"),
        )
        task_id = cursor.lastrowid
        cursor.execute(
            "UPDATE communications SET related_task_id = ? WHERE id = ?",
            (task_id, communication_id),
        )

    db.commit()
    return {"communication_id": communication_id}


@mcp.tool()
def list_open_tasks() -> list[dict]:
    """List all open tasks, ordered by due date."""
    cursor = db.cursor()
    cursor.execute(
        """SELECT tasks.id, tasks.application_id, tasks.type, tasks.due_date, tasks.notes
           FROM tasks
           WHERE tasks.status = 'open'
           ORDER BY tasks.due_date"""
    )
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@mcp.tool()
def mark_task_complete(task_id: int) -> dict:
    """Mark a task as complete."""
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET status = 'complete' WHERE id = ?", (task_id,))
    db.commit()
    return {"task_id": task_id, "status": "complete"}


if __name__ == "__main__":
    mcp.run()
