# Job Hunt Tracker

A personal practice project using Claude.ai and Code that will help me learn how to use a common
real data architecture pattern: an API layer, an MCP server, a database, and an AI agent, all working together.

This project is a way to learn how these pieces connect,
not a production tool.

## Status

Database schema designed and reviewed (six related tables: companies,
postings, requirements, applications, tasks, communications) and
version-controlled in `schema.sql`. A local SQLite database has been
built from that schema using a small Python script (`init_db.py`). 
Sample data has been created in `seed_data.py` to populate the database. 

The MCP server (`server.py`) is built and working with eight tools:
searching live job postings through the Adzuna API, saving postings,
logging applications and communications (with automatic follow-up task
creation), listing open tasks, marking tasks complete, and listing saved
postings and applications. The server is registered with Claude Desktop,
so the full API -> MCP server -> database -> agent pattern is working
end to end.

A learning log has been created within a Claude.ai project relating to
this project. This tracks specific moments where a decision or mistake
brings up teaching points. This is kept separate from the repo itself.

Next: add the ability to edit or update existing records (currently only specific workflow actions are supported, not general editing), and buils a data-viz layer to make stored data easier to review.