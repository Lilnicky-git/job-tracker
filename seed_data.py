import sqlite3

connection = sqlite3.connect("tracker.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

cursor.execute(
    "INSERT INTO companies (name, industry, notes) VALUES (?, ?, ?)",
    ("Acme Robotics", "Manufacturing", "Found through a general job board search.")
)
acme_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO companies (name, industry, notes) VALUES (?, ?, ?)",
    ("Blue Ridge Analytics", "Data Analytics", "Small analytics consulting firm.")
)
blue_ridge_id = cursor.lastrowid

cursor.execute(
    """INSERT INTO postings (company_id, title, location, salary_min, salary_max, source_url, date_found, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (acme_id, "Data Analyst", "Remote", 60000, 80000, "https://example.com/job/123", "2026-07-10", "matched")
)
acme_posting_id = cursor.lastrowid

cursor.execute(
    """INSERT INTO postings (company_id, title, location, salary_min, salary_max, source_url, date_found, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (blue_ridge_id, "Junior Data Analyst", "Charlotte, NC", 50000, 65000, "https://example.com/job/456", "2026-07-15", "new")
)
blue_ridge_posting_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO requirements (posting_id, requirement, must_have) VALUES (?, ?, ?)",
    (acme_posting_id, "2+ years of SQL experience", 1)
)
cursor.execute(
    "INSERT INTO requirements (posting_id, requirement, must_have) VALUES (?, ?, ?)",
    (acme_posting_id, "Bachelor's degree in a related field", 1)
)
cursor.execute(
    "INSERT INTO requirements (posting_id, requirement, must_have) VALUES (?, ?, ?)",
    (acme_posting_id, "Experience with Python", 0)
)

cursor.execute(
    "INSERT INTO applications (posting_id, date_applied, stage, notes) VALUES (?, ?, ?, ?)",
    (acme_posting_id, "2026-07-12", "interview", "Phone screen scheduled.")
)
acme_application_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO tasks (application_id, type, due_date, status, notes) VALUES (?, ?, ?, ?, ?)",
    (acme_application_id, "Prepare for phone screen", "2026-07-22", "open", "Review common data analyst interview questions.")
)
task_id = cursor.lastrowid

cursor.execute(
    """INSERT INTO communications (application_id, date, type, direction, summary, follow_up_required, related_task_id)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    (acme_application_id, "2026-07-11", "email", "inbound", "Recruiter reached out to schedule a phone screen.", 1, task_id)
)

connection.commit()
connection.close()

print("Sample data inserted successfully.")
